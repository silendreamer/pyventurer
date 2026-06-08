from app.models.domain import LearnerProfile, Recommendation
from app.repositories.content_repository import ContentRepository, content_repository


class RecommendationService:
    def __init__(self, repository: ContentRepository) -> None:
        self.repository = repository

    def recommend(self, profile: LearnerProfile) -> list[Recommendation]:
        course = self.repository.get_course("python-demo")
        reason = self._build_reason(profile)
        return [
            Recommendation(
                course=course,
                starting_lesson_id="lesson-print",
                starting_exercise_id="exercise-print-hello",
                reason=reason,
                next_steps=[
                    "Take the short Python placement check",
                    "Try the print() sample lesson",
                    "Create an account only when you are ready to save progress",
                ],
            )
        ]

    def _build_reason(self, profile: LearnerProfile) -> str:
        if profile.experience_level == "new":
            return "This path starts with real Python basics and gives quick feedback."
        if profile.learning_goal == "automation":
            return "Python is a strong first step for scripts and automation tools."
        if profile.learning_goal == "ai":
            return "Python basics are the foundation for later AI builder paths."
        return "This tiny path proves the platform flow before larger courses are added."


recommendation_service = RecommendationService(content_repository)
