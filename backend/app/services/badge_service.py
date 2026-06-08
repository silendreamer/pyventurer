from app.models.badges import BADGE_DEFINITIONS
from app.models.domain import Badge, ProgressState
from app.repositories.progress_repository import ProgressRepository, progress_repository


class BadgeService:
    def __init__(self, progress: ProgressRepository) -> None:
        self.progress = progress

    def get_badge(self, badge_id: str) -> Badge | None:
        return BADGE_DEFINITIONS.get(badge_id)

    def award_for_exercise(self, anonymous_user_id: str) -> ProgressState:
        return self.progress.award_badge(anonymous_user_id, BADGE_DEFINITIONS["first-code-run"])

    def award_for_quiz(self, anonymous_user_id: str, score: int) -> ProgressState:
        progress = self.progress.get_progress(anonymous_user_id)
        if score == 100:
            progress = self.progress.award_badge(anonymous_user_id, BADGE_DEFINITIONS["perfect-quiz"])
        if progress.completed_lessons and progress.completed_quizzes:
            progress = self.progress.award_badge(anonymous_user_id, BADGE_DEFINITIONS["python-starter"])
        return progress


badge_service = BadgeService(progress_repository)
