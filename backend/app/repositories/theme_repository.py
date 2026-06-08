from app.models.domain import Theme, ThemeTokens


class ThemeRepository:
    def __init__(self) -> None:
        self.themes = [
            Theme(
                id="explorer",
                name="Explorer",
                slug="explorer",
                description="Open, bright, and discovery-focused.",
                icon_style="line",
                illustration_style="maps and path markers",
                layout_density="comfortable",
                tone="curious",
                tokens=ThemeTokens(
                    primary="#0f766e",
                    secondary="#2563eb",
                    accent="#f59e0b",
                    background="#f7fbf9",
                    surface="#ffffff",
                    text="#10201f",
                    muted="#60706d",
                    code_background="#101827",
                    hero_image="linear-gradient(135deg, #dff7ef 0%, #dbeafe 60%, #fff7ed 100%)",
                    lesson_image="radial-gradient(circle at 25% 20%, #fbbf24 0 8%, transparent 9%), linear-gradient(135deg, #ccfbf1, #bfdbfe)",
                ),
            ),
            Theme(
                id="builder",
                name="Builder",
                slug="builder",
                description="Structured, practical, and project-minded.",
                icon_style="solid",
                illustration_style="blueprints and modules",
                layout_density="dense",
                tone="direct",
                tokens=ThemeTokens(
                    primary="#14532d",
                    secondary="#334155",
                    accent="#d97706",
                    background="#f8fafc",
                    surface="#ffffff",
                    text="#111827",
                    muted="#64748b",
                    code_background="#111827",
                    hero_image="linear-gradient(135deg, #dcfce7 0%, #e2e8f0 55%, #fef3c7 100%)",
                    lesson_image="repeating-linear-gradient(90deg, rgba(20,83,45,.12) 0 1px, transparent 1px 32px), linear-gradient(135deg, #f8fafc, #dcfce7)",
                ),
            ),
            Theme(
                id="minimal",
                name="Minimal",
                slug="minimal",
                description="Quiet, focused, and distraction-light.",
                icon_style="outline",
                illustration_style="simple geometric",
                layout_density="spacious",
                tone="calm",
                tokens=ThemeTokens(
                    primary="#111827",
                    secondary="#0f766e",
                    accent="#2563eb",
                    background="#f9fafb",
                    surface="#ffffff",
                    text="#111827",
                    muted="#6b7280",
                    code_background="#0b1020",
                    hero_image="linear-gradient(135deg, #ffffff 0%, #f3f4f6 60%, #e0f2fe 100%)",
                    lesson_image="linear-gradient(135deg, #f9fafb, #e5e7eb)",
                ),
            ),
        ]

    def list_themes(self) -> list[Theme]:
        return self.themes

    def get_theme(self, theme_id: str) -> Theme:
        return next(theme for theme in self.themes if theme.id == theme_id)


theme_repository = ThemeRepository()
