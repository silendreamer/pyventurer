from app.repositories.progress_repository import ProgressRepository, progress_repository


class ProgressService:
    def __init__(self, repository: ProgressRepository) -> None:
        self.repository = repository

    def get_progress(self, anonymous_user_id: str):
        return self.repository.get_progress(anonymous_user_id)

    def get_progress_for_user(self, user_id: str):
        return self.repository.get_progress_for_user(user_id)

    def complete_lesson(self, anonymous_user_id: str, lesson_id: str):
        return self.repository.complete_lesson(anonymous_user_id, lesson_id)


progress_service = ProgressService(progress_repository)
