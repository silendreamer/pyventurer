from app.models.domain import Badge, ProgressState
from app.repositories.progress_repository import ProgressRepository, progress_repository


class BadgeService:
    def __init__(self, progress: ProgressRepository) -> None:
        self.progress = progress
        self.badges = {
            "first-code-run": Badge(
                id="first-code-run",
                title="First Code Run",
                description="Ran and passed a first coding exercise.",
                icon="play",
            ),
            "python-starter": Badge(
                id="python-starter",
                title="Python Starter",
                description="Completed the first lesson and quiz.",
                icon="spark",
            ),
            "perfect-quiz": Badge(
                id="perfect-quiz",
                title="Perfect Quiz",
                description="Scored 100% on a quiz.",
                icon="check",
            ),
        }

    def award_for_exercise(self, anonymous_user_id: str) -> ProgressState:
        return self.progress.award_badge(anonymous_user_id, self.badges["first-code-run"])

    def award_for_quiz(self, anonymous_user_id: str, score: int) -> ProgressState:
        progress = self.progress.get_progress(anonymous_user_id)
        if score == 100:
            progress = self.progress.award_badge(anonymous_user_id, self.badges["perfect-quiz"])
        if progress.completed_lessons and progress.completed_quizzes:
            progress = self.progress.award_badge(anonymous_user_id, self.badges["python-starter"])
        return progress


badge_service = BadgeService(progress_repository)
