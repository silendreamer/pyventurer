import json
import sqlite3
from typing import NoReturn

from fastapi import HTTPException

from app.db.connection import get_connection
from app.models.domain import (
    Course,
    Exercise,
    Language,
    Lesson,
    PlacementAssessment,
    PlacementQuestion,
    Quiz,
    QuizQuestionWithAnswer,
)


def _not_found(entity: str, identifier: str) -> NoReturn:
    raise HTTPException(status_code=404, detail=f"{entity} '{identifier}' not found")


class ContentRepository:
    def __init__(self, connection: sqlite3.Connection | None = None) -> None:
        self.connection = connection or get_connection()

    def list_languages(self) -> list[Language]:
        rows = self.connection.execute("SELECT * FROM languages ORDER BY order_index, name").fetchall()
        return [self._language_from_row(row) for row in rows]

    def list_courses(self) -> list[Course]:
        rows = self.connection.execute("SELECT * FROM courses ORDER BY order_index, title").fetchall()
        return [self._course_from_row(row) for row in rows]

    def get_course(self, course_id: str) -> Course:
        row = self.connection.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
        return self._course_from_row(row) if row else _not_found("Course", course_id)

    def get_course_by_slug(self, slug: str) -> Course:
        row = self.connection.execute("SELECT * FROM courses WHERE slug = ?", (slug,)).fetchone()
        return self._course_from_row(row) if row else _not_found("Course", slug)

    def get_lesson(self, lesson_id_or_slug: str) -> Lesson:
        row = self.connection.execute(
            "SELECT * FROM lessons WHERE id = ? OR slug = ?",
            (lesson_id_or_slug, lesson_id_or_slug),
        ).fetchone()
        return self._lesson_from_row(row) if row else _not_found("Lesson", lesson_id_or_slug)

    def get_exercise(self, exercise_id_or_slug: str) -> Exercise:
        row = self.connection.execute(
            "SELECT * FROM exercises WHERE id = ? OR slug = ?",
            (exercise_id_or_slug, exercise_id_or_slug),
        ).fetchone()
        return self._exercise_from_row(row) if row else _not_found("Exercise", exercise_id_or_slug)

    def get_quiz(self, quiz_id_or_slug: str) -> Quiz:
        row = self.connection.execute(
            "SELECT * FROM quizzes WHERE id = ? OR slug = ?",
            (quiz_id_or_slug, quiz_id_or_slug),
        ).fetchone()
        if not row:
            _not_found("Quiz", quiz_id_or_slug)
        return self._quiz_from_row(row)

    def get_placement_for_course(self, course_id: str) -> PlacementAssessment:
        row = self.connection.execute(
            "SELECT * FROM placement_assessments WHERE course_id = ? ORDER BY rowid LIMIT 1",
            (course_id,),
        ).fetchone()
        if not row:
            _not_found("Placement", course_id)
        question_rows = self.connection.execute(
            "SELECT * FROM placement_questions WHERE assessment_id = ? ORDER BY order_index",
            (row["id"],),
        ).fetchall()
        return PlacementAssessment(
            id=row["id"],
            course_id=row["course_id"],
            title=row["title"],
            passing_score=row["passing_score"],
            questions=[
                PlacementQuestion(
                    id=question["id"],
                    prompt=question["prompt"],
                    choices=json.loads(question["choices"]),
                    correct_choice=question["correct_choice"],
                )
                for question in question_rows
            ],
        )

    def get_first_lesson_for_course(self, course_id: str) -> Lesson:
        row = self.connection.execute(
            """
            SELECT lessons.*
            FROM lessons
            JOIN exercises ON exercises.lesson_id = lessons.id
            WHERE lessons.course_id = ? AND lessons.status = 'published' AND exercises.status = 'published'
            ORDER BY lessons.order_index, exercises.order_index
            LIMIT 1
            """,
            (course_id,),
        ).fetchone()
        if not row:
            row = self.connection.execute(
                "SELECT * FROM lessons WHERE course_id = ? ORDER BY order_index LIMIT 1",
                (course_id,),
            ).fetchone()
        return self._lesson_from_row(row) if row else _not_found("Lesson for course", course_id)

    def get_first_exercise_for_lesson(self, lesson_id: str) -> Exercise:
        row = self.connection.execute(
            "SELECT * FROM exercises WHERE lesson_id = ? AND status = 'published' ORDER BY order_index LIMIT 1",
            (lesson_id,),
        ).fetchone()
        return self._exercise_from_row(row) if row else _not_found("Exercise for lesson", lesson_id)

    def get_first_quiz_for_lesson(self, lesson_id: str) -> Quiz:
        lesson = self.get_lesson(lesson_id)
        row = self.connection.execute(
            """
            SELECT quizzes.*
            FROM quizzes
            JOIN modules ON modules.id = quizzes.module_id
            WHERE modules.id = (
                SELECT module_id FROM lessons WHERE id = ?
            )
            ORDER BY quizzes.order_index
            LIMIT 1
            """,
            (lesson.id,),
        ).fetchone()
        return self._quiz_from_row(row) if row else _not_found("Quiz for lesson", lesson_id)

    def get_curriculum_tree(self) -> dict:
        languages = []
        for language in self.connection.execute(
            "SELECT * FROM languages WHERE is_active = 1 ORDER BY order_index, name"
        ).fetchall():
            language_courses = []
            for course in self.connection.execute(
                "SELECT * FROM courses WHERE language_id = ? ORDER BY order_index, title",
                (language["id"],),
            ).fetchall():
                modules = self._outline_modules(course["id"])
                language_courses.append(
                    {
                        "id": course["id"],
                        "title": course["title"],
                        "slug": course["slug"],
                        "description": course["description"],
                        "status": course["status"],
                        "modules": modules,
                        "next_course_slug": course["next_course_slug"],
                    }
                )
            languages.append(
                {
                    "id": language["id"],
                    "title": language["name"],
                    "description": language["description"],
                    "status": language["status"],
                    "courses": language_courses,
                }
            )
        return {"languages": languages}

    def get_course_outline(self, course_slug: str) -> dict:
        course = self.get_course_by_slug(course_slug)
        next_course = None
        if course.next_course_slug:
            next_row = self.connection.execute(
                "SELECT id, title, slug, description, status FROM courses WHERE slug = ?",
                (course.next_course_slug,),
            ).fetchone()
            if next_row:
                next_course = dict(next_row)
        completion = self.connection.execute(
            "SELECT * FROM course_completion_rules WHERE course_id = ?",
            (course.id,),
        ).fetchone()
        return {
            "course": course,
            "modules": self._outline_modules(course.id),
            "next_course": next_course,
            "completion_rules": dict(completion) if completion else None,
        }

    def get_project(self, project_slug: str) -> dict:
        row = self.connection.execute(
            "SELECT * FROM projects WHERE id = ? OR slug = ?",
            (project_slug, project_slug),
        ).fetchone()
        return dict(row) if row else _not_found("Project", project_slug)

    def get_course_completion_rules(self, course_slug: str) -> dict:
        course = self.get_course_by_slug(course_slug)
        row = self.connection.execute(
            "SELECT * FROM course_completion_rules WHERE course_id = ?",
            (course.id,),
        ).fetchone()
        return dict(row) if row else _not_found("Completion rules", course_slug)

    def _outline_modules(self, course_id: str) -> list[dict]:
        modules = []
        for module in self.connection.execute(
            "SELECT * FROM modules WHERE course_id = ? ORDER BY order_index",
            (course_id,),
        ).fetchall():
            lessons = [
                {
                    "id": lesson["id"],
                    "title": lesson["title"],
                    "slug": lesson["slug"],
                    "topic": lesson["topic"],
                    "description": lesson["short_description"],
                    "status": lesson["status"],
                    "order_index": lesson["order_index"],
                    "implemented": self._lesson_has_published_exercise(lesson["id"]),
                }
                for lesson in self.connection.execute(
                    "SELECT * FROM lessons WHERE module_id = ? ORDER BY order_index",
                    (module["id"],),
                ).fetchall()
            ]
            projects = [
                {
                    "id": project["id"],
                    "title": project["title"],
                    "slug": project["slug"],
                    "description": project["description"],
                    "type": project["project_type"],
                    "status": project["status"],
                    "order_index": project["order_index"],
                }
                for project in self.connection.execute(
                    "SELECT * FROM projects WHERE module_id = ? ORDER BY order_index",
                    (module["id"],),
                ).fetchall()
            ]
            quiz = self.connection.execute(
                "SELECT id, title, slug, status FROM quizzes WHERE module_id = ? ORDER BY order_index LIMIT 1",
                (module["id"],),
            ).fetchone()
            modules.append(
                {
                    "id": module["id"],
                    "title": module["title"],
                    "slug": module["slug"],
                    "description": module["description"],
                    "status": module["status"],
                    "order_index": module["order_index"],
                    "lessons": lessons,
                    "projects": projects,
                    "quiz": dict(quiz) if quiz else None,
                }
            )
        return modules

    def _lesson_has_published_exercise(self, lesson_id: str) -> bool:
        row = self.connection.execute(
            "SELECT 1 FROM exercises WHERE lesson_id = ? AND status = 'published' LIMIT 1",
            (lesson_id,),
        ).fetchone()
        return row is not None

    def _language_from_row(self, row: sqlite3.Row) -> Language:
        return Language(
            id=row["id"],
            name=row["name"],
            slug=row["slug"],
            description=row["description"],
            is_active=bool(row["is_active"]),
        )

    def _course_from_row(self, row: sqlite3.Row) -> Course:
        return Course(
            id=row["id"],
            language_id=row["language_id"],
            title=row["title"],
            slug=row["slug"],
            description=row["description"],
            target_audience=row["target_audience"],
            difficulty=row["difficulty"],
            estimated_duration=row["estimated_duration"],
            outcomes=[
                "Understand basic Python syntax",
                "Write and run small programs",
                "Build small command-line projects",
            ],
            status=row["status"],
            course_goal=row["course_goal"],
            next_course_slug=row["next_course_slug"],
            is_active=row["status"] != "locked",
        )

    def _lesson_from_row(self, row: sqlite3.Row) -> Lesson:
        code_examples = [row["example_code"]] if row["example_code"] else []
        return Lesson(
            id=row["id"],
            course_id=row["course_id"],
            topic=row["topic"],
            title=row["title"],
            body=row["body"],
            code_examples=code_examples,
            estimated_minutes=row["estimated_minutes"],
            slug=row["slug"],
            short_description=row["short_description"],
            learning_objective=row["learning_objective"],
            status=row["status"],
            order_index=row["order_index"],
        )

    def _exercise_from_row(self, row: sqlite3.Row) -> Exercise:
        return Exercise(
            id=row["id"],
            lesson_id=row["lesson_id"],
            title=row["title"],
            instructions=row["instructions"],
            starter_code=row["starter_code"],
            language_id=row["language_id"],
            grader_type=row["grader_type"],
            grader_config=json.loads(row["grader_config"]),
            slug=row["slug"],
            status=row["status"],
            order_index=row["order_index"],
        )

    def _quiz_from_row(self, row: sqlite3.Row) -> Quiz:
        questions = []
        for question in self.connection.execute(
            "SELECT * FROM quiz_questions WHERE quiz_id = ? ORDER BY order_index",
            (row["id"],),
        ).fetchall():
            choices = self.connection.execute(
                "SELECT * FROM quiz_answer_choices WHERE question_id = ? ORDER BY order_index",
                (question["id"],),
            ).fetchall()
            correct_choice = next(choice["choice_text"] for choice in choices if choice["is_correct"])
            questions.append(
                QuizQuestionWithAnswer(
                    id=question["id"],
                    prompt=question["prompt"],
                    choices=[choice["choice_text"] for choice in choices],
                    correct_choice=correct_choice,
                    explanation=question["explanation"],
                )
            )
        return Quiz(
            id=row["id"],
            lesson_id=row["lesson_id"] or "",
            title=row["title"],
            passing_score=row["passing_score"],
            questions=questions,
            slug=row["slug"],
            module_id=row["module_id"],
            status=row["status"],
        )


content_repository = ContentRepository()
