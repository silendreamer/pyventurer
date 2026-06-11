from app.repositories.content_repository import ContentRepository, content_repository


class ContentService:
    def __init__(self, repository: ContentRepository) -> None:
        self.repository = repository

    def get_catalog(self) -> dict:
        return {
            "languages": self.repository.list_languages(),
            "courses": self.repository.list_courses(),
        }

    def get_course_overview(self, slug: str) -> dict:
        course = self.repository.get_course_by_slug(slug)
        lesson = self.repository.get_first_lesson_for_course(course.id)
        exercise = self.repository.get_first_exercise_for_lesson(lesson.id)
        quiz = self.repository.get_first_quiz_for_lesson(lesson.id)
        return {
            "course": course,
            "lesson": lesson,
            "exercise": exercise,
            "quiz": {"id": quiz.id, "title": quiz.title, "passing_score": quiz.passing_score},
        }

    def get_lesson_bundle(self, lesson_id: str) -> dict:
        lesson = self.repository.get_lesson(lesson_id)
        exercise = self.repository.get_first_exercise_for_lesson(lesson.id)
        quiz = self.repository.get_first_quiz_for_lesson(lesson.id)
        return {
            "lesson": lesson,
            "exercise": exercise,
            "quiz": {"id": quiz.id, "title": quiz.title, "passing_score": quiz.passing_score},
        }

    def get_curriculum_tree(self) -> dict:
        return self.repository.get_curriculum_tree()

    def get_course_outline(self, course_slug: str) -> dict:
        return self.repository.get_course_outline(course_slug)

    def get_project(self, project_slug: str) -> dict:
        return self.repository.get_project(project_slug)

    def get_course_completion(self, course_slug: str) -> dict:
        return self.repository.get_course_completion_rules(course_slug)


content_service = ContentService(content_repository)
