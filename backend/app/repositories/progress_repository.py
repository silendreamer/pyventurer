from app.models.domain import Badge, LearnerProfile, ProgressState


class ProgressRepository:
    def __init__(self) -> None:
        self.profiles: dict[str, LearnerProfile] = {}
        self.progress: dict[str, ProgressState] = {}

    def save_profile(self, anonymous_user_id: str, profile: LearnerProfile) -> LearnerProfile:
        self.profiles[anonymous_user_id] = profile
        self._ensure_progress(anonymous_user_id)
        return profile

    def get_profile(self, anonymous_user_id: str) -> LearnerProfile | None:
        return self.profiles.get(anonymous_user_id)

    def update_theme(self, anonymous_user_id: str, theme_id: str) -> LearnerProfile | None:
        profile = self.profiles.get(anonymous_user_id)
        if profile is None:
            return None
        updated = profile.model_copy(update={"selected_theme_id": theme_id})
        self.profiles[anonymous_user_id] = updated
        return updated

    def get_progress(self, anonymous_user_id: str) -> ProgressState:
        return self._ensure_progress(anonymous_user_id)

    def record_placement(self, anonymous_user_id: str, assessment_id: str, score: int) -> ProgressState:
        progress = self._ensure_progress(anonymous_user_id)
        progress.placement_scores[assessment_id] = score
        progress.xp = max(progress.xp, 10)
        return progress

    def complete_lesson(self, anonymous_user_id: str, lesson_id: str) -> ProgressState:
        progress = self._ensure_progress(anonymous_user_id)
        if lesson_id not in progress.completed_lessons:
            progress.completed_lessons.append(lesson_id)
            progress.xp += 15
        return progress

    def complete_exercise(self, anonymous_user_id: str, exercise_id: str) -> ProgressState:
        progress = self._ensure_progress(anonymous_user_id)
        if exercise_id not in progress.completed_exercises:
            progress.completed_exercises.append(exercise_id)
            progress.xp += 25
            progress.streak = max(progress.streak, 1)
        return progress

    def complete_quiz(self, anonymous_user_id: str, quiz_id: str) -> ProgressState:
        progress = self._ensure_progress(anonymous_user_id)
        if quiz_id not in progress.completed_quizzes:
            progress.completed_quizzes.append(quiz_id)
            progress.xp += 20
        return progress

    def award_badge(self, anonymous_user_id: str, badge: Badge) -> ProgressState:
        progress = self._ensure_progress(anonymous_user_id)
        if badge.id not in {existing.id for existing in progress.badges}:
            progress.badges.append(badge)
        return progress

    def _ensure_progress(self, anonymous_user_id: str) -> ProgressState:
        if anonymous_user_id not in self.progress:
            self.progress[anonymous_user_id] = ProgressState(
                anonymous_user_id=anonymous_user_id,
                xp=0,
                streak=0,
                completed_lessons=[],
                completed_exercises=[],
                completed_quizzes=[],
                placement_scores={},
                badges=[],
            )
        return self.progress[anonymous_user_id]


progress_repository = ProgressRepository()
