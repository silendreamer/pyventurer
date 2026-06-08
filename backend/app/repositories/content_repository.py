from typing import NoReturn

from fastapi import HTTPException

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
    def __init__(self) -> None:
        self.languages = [
            Language(
                id="python",
                name="Python",
                slug="python",
                description="Learn practical Python skills from your first print statement to real projects.",
            ),
            Language(
                id="javascript",
                name="JavaScript",
                slug="javascript",
                description="Future curriculum placeholder for web programming.",
                is_active=False,
            ),
            Language(
                id="sql",
                name="SQL",
                slug="sql",
                description="Future curriculum placeholder for data querying.",
                is_active=False,
            ),
            Language(
                id="ai-agents",
                name="AI Agents",
                slug="ai-agents",
                description="Future curriculum placeholder for agentic systems.",
                is_active=False,
            ),
        ]
        self.courses = [
            Course(
                id="python-demo",
                language_id="python",
                title="Python for Beginners",
                slug="python-demo-path",
                description="A tiny beginner path that proves the PyVenturer framework works end-to-end.",
                target_audience="New Python learners",
                difficulty="Beginner",
                estimated_duration="20 minutes",
                outcomes=[
                    "Run a real Python print statement",
                    "Explain what output means",
                    "Complete a first quiz and earn starter XP",
                ],
            )
        ]
        self.lessons = [
            Lesson(
                id="lesson-print",
                course_id="python-demo",
                topic="print()",
                title="What is print()?",
                body=(
                    "The print() function sends text to the output. It is often the first real "
                    "Python tool learners use because it gives immediate feedback."
                ),
                code_examples=['print("Hello World")', 'print("I can build with Python")'],
                estimated_minutes=4,
            )
        ]
        self.exercises = [
            Exercise(
                id="exercise-print-hello",
                lesson_id="lesson-print",
                title="Print Hello World",
                instructions='Write Python code that prints exactly: Hello World',
                starter_code='print("Hello World")',
                language_id="python",
                grader_type="output_match",
                grader_config={"expected_output": "Hello World"},
            )
        ]
        self.quizzes = [
            Quiz(
                id="quiz-print-basics",
                lesson_id="lesson-print",
                title="print() Basics Check",
                passing_score=100,
                questions=[
                    QuizQuestionWithAnswer(
                        id="q1",
                        prompt="What does print() do?",
                        choices=[
                            "Shows output",
                            "Creates a file",
                            "Starts a website",
                        ],
                        correct_choice="Shows output",
                        explanation="print() displays a value in the output.",
                    ),
                    QuizQuestionWithAnswer(
                        id="q2",
                        prompt='Which code prints Hello World?',
                        choices=[
                            'print("Hello World")',
                            'move_right("Hello World")',
                            'collect_gem("Hello World")',
                        ],
                        correct_choice='print("Hello World")',
                        explanation="This is real Python syntax for displaying text.",
                    ),
                ],
            )
        ]
        self.placement_assessments = [
            PlacementAssessment(
                id="placement-python-demo",
                course_id="python-demo",
                title="Python Starting Point Check",
                passing_score=67,
                questions=[
                    PlacementQuestion(
                        id="p1",
                        prompt="Have you written Python before?",
                        choices=["Not yet", "A little", "Often"],
                        correct_choice="A little",
                    ),
                    PlacementQuestion(
                        id="p2",
                        prompt='What is the output of print("Hi")?',
                        choices=["Hi", '"Hi"', "print"],
                        correct_choice="Hi",
                    ),
                    PlacementQuestion(
                        id="p3",
                        prompt="Which is a real Python concept?",
                        choices=["variables", "collect_gem", "turn_left"],
                        correct_choice="variables",
                    ),
                ],
            )
        ]
        self.curriculum_tree = {
            "languages": [
                {
                    "id": "python",
                    "title": "Python",
                    "description": "Learn Python from beginner fundamentals to applied tracks.",
                    "courses": [
                        {
                            "id": "python-demo",
                            "title": "Python for Beginners",
                            "slug": "python-demo-path",
                            "description": "Start with practical Python fundamentals.",
                            "modules": [
                                {
                                    "id": "python-basics",
                                    "title": "Python Basics",
                                    "description": "First concepts every Python learner needs.",
                                    "lessons": [
                                        {
                                            "id": "lesson-print",
                                            "title": "Print output",
                                            "topic": "print()",
                                            "implemented": True,
                                        },
                                        {
                                            "id": "lesson-variables",
                                            "title": "Variables",
                                            "topic": "variables",
                                            "implemented": False,
                                        },
                                        {
                                            "id": "lesson-strings",
                                            "title": "Strings",
                                            "topic": "strings",
                                            "implemented": False,
                                        },
                                    ],
                                },
                                {
                                    "id": "control-flow",
                                    "title": "Control Flow",
                                    "description": "Make programs branch and repeat.",
                                    "lessons": [
                                        {
                                            "id": "lesson-conditionals",
                                            "title": "Conditionals",
                                            "topic": "if statements",
                                            "implemented": False,
                                        },
                                        {
                                            "id": "lesson-loops",
                                            "title": "Loops",
                                            "topic": "for and while loops",
                                            "implemented": False,
                                        },
                                        {
                                            "id": "lesson-functions",
                                            "title": "Functions",
                                            "topic": "functions",
                                            "implemented": False,
                                        },
                                    ],
                                },
                            ],
                        },
                        {
                            "id": "python-advanced",
                            "title": "Python Advanced",
                            "slug": "python-advanced",
                            "description": "Future path for deeper Python skills.",
                            "modules": [
                                {
                                    "id": "advanced-structures",
                                    "title": "Data Structures",
                                    "description": "Lists, dictionaries, files, and modules.",
                                    "lessons": [
                                        {
                                            "id": "lesson-lists",
                                            "title": "Lists",
                                            "topic": "lists",
                                            "implemented": False,
                                        },
                                        {
                                            "id": "lesson-dictionaries",
                                            "title": "Dictionaries",
                                            "topic": "dictionaries",
                                            "implemented": False,
                                        },
                                        {
                                            "id": "lesson-files",
                                            "title": "Files",
                                            "topic": "files",
                                            "implemented": False,
                                        },
                                    ],
                                }
                            ],
                        },
                        {
                            "id": "python-data-science",
                            "title": "Python for Data Science",
                            "slug": "python-data-science",
                            "description": "Future path for analysis and visualization.",
                            "modules": [
                                {
                                    "id": "data-foundations",
                                    "title": "Data Foundations",
                                    "description": "Prepare for real data work.",
                                    "lessons": [
                                        {
                                            "id": "lesson-data-lists",
                                            "title": "Working with datasets",
                                            "topic": "datasets",
                                            "implemented": False,
                                        },
                                        {
                                            "id": "lesson-pandas-intro",
                                            "title": "Intro to pandas",
                                            "topic": "pandas",
                                            "implemented": False,
                                        },
                                    ],
                                }
                            ],
                        },
                    ],
                }
            ]
        }

    def list_languages(self) -> list[Language]:
        return self.languages

    def list_courses(self) -> list[Course]:
        return self.courses

    def get_course(self, course_id: str) -> Course:
        return next((course for course in self.courses if course.id == course_id), None) or _not_found("Course", course_id)

    def get_course_by_slug(self, slug: str) -> Course:
        return next((course for course in self.courses if course.slug == slug), None) or _not_found("Course", slug)

    def get_lesson(self, lesson_id: str) -> Lesson:
        return next((lesson for lesson in self.lessons if lesson.id == lesson_id), None) or _not_found("Lesson", lesson_id)

    def get_exercise(self, exercise_id: str) -> Exercise:
        return next((exercise for exercise in self.exercises if exercise.id == exercise_id), None) or _not_found("Exercise", exercise_id)

    def get_quiz(self, quiz_id: str) -> Quiz:
        return next((quiz for quiz in self.quizzes if quiz.id == quiz_id), None) or _not_found("Quiz", quiz_id)

    def get_placement_for_course(self, course_id: str) -> PlacementAssessment:
        return next((a for a in self.placement_assessments if a.course_id == course_id), None) or _not_found("Placement", course_id)

    def get_first_lesson_for_course(self, course_id: str) -> Lesson:
        return next((l for l in self.lessons if l.course_id == course_id), None) or _not_found("Lesson for course", course_id)

    def get_first_exercise_for_lesson(self, lesson_id: str) -> Exercise:
        return next((e for e in self.exercises if e.lesson_id == lesson_id), None) or _not_found("Exercise for lesson", lesson_id)

    def get_first_quiz_for_lesson(self, lesson_id: str) -> Quiz:
        return next((q for q in self.quizzes if q.lesson_id == lesson_id), None) or _not_found("Quiz for lesson", lesson_id)

    def get_curriculum_tree(self) -> dict:
        return self.curriculum_tree


content_repository = ContentRepository()
