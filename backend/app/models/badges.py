from app.models.domain import Badge

BADGE_DEFINITIONS: dict[str, Badge] = {
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
