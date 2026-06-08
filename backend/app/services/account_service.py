from app.repositories.progress_repository import ProgressRepository, progress_repository


class AccountService:
    def __init__(self, progress: ProgressRepository) -> None:
        self.progress = progress

    def create_placeholder_account(self, anonymous_user_id: str, email: str, name: str) -> dict:
        return {
            "status": "created",
            "message": "MVP placeholder account created. Progress is ready to save when auth is implemented.",
            "user": {"id": anonymous_user_id, "email": email, "name": name},
            "progress": self.progress.get_progress(anonymous_user_id),
        }


account_service = AccountService(progress_repository)
