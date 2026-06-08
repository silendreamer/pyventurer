from app.models.domain import Theme
from app.repositories.progress_repository import ProgressRepository, progress_repository
from app.repositories.theme_repository import ThemeRepository, theme_repository


class ThemeService:
    def __init__(self, themes: ThemeRepository, progress: ProgressRepository) -> None:
        self.themes = themes
        self.progress = progress

    def list_themes(self) -> list[Theme]:
        return self.themes.list_themes()

    def select_theme(self, anonymous_user_id: str, theme_id: str) -> Theme:
        theme = self.themes.get_theme(theme_id)
        self.progress.update_theme(anonymous_user_id, theme.id)
        return theme

    def resolve_for_user(self, anonymous_user_id: str) -> Theme:
        profile = self.progress.get_profile(anonymous_user_id)
        if profile:
            return self.themes.get_theme(profile.selected_theme_id)
        return self.themes.get_theme("explorer")


theme_service = ThemeService(theme_repository, progress_repository)
