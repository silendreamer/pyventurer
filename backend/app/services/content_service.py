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
        lesson = next(lesson for lesson in self.repository.lessons if lesson.course_id == course.id)
        exercise = next(exercise for exercise in self.repository.exercises if exercise.lesson_id == lesson.id)
        quiz = next(quiz for quiz in self.repository.quizzes if quiz.lesson_id == lesson.id)
        return {
            "course": course,
            "lesson": lesson,
            "exercise": exercise,
            "quiz": {"id": quiz.id, "title": quiz.title, "passing_score": quiz.passing_score},
        }

    def get_curriculum_tree(self) -> dict:
        return self.repository.get_curriculum_tree()


content_service = ContentService(content_repository)
