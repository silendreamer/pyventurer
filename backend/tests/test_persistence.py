from app.models.badges import BADGE_DEFINITIONS
from app.models.domain import LearnerProfile
from app.repositories.progress_repository import progress_repository


def test_profile_survives_round_trip():
    profile = LearnerProfile(
        age_range="teen-adult",
        experience_level="some",
        learning_goal="data",
        motivation_type="create-real-projects",
        preferred_style="minimal",
        selected_theme_id="builder",
    )
    progress_repository.save_profile("persist-user", profile)
    loaded = progress_repository.get_profile("persist-user")

    assert loaded is not None
    assert loaded.age_range == "teen-adult"
    assert loaded.selected_theme_id == "builder"


def test_progress_idempotent_lesson_completion():
    progress_repository.complete_lesson("idem-user", "lesson-1")
    progress_repository.complete_lesson("idem-user", "lesson-1")
    progress = progress_repository.get_progress("idem-user")

    assert progress.completed_lessons.count("lesson-1") == 1
    assert progress.xp == 15


def test_badge_hydration():
    progress_repository.award_badge("badge-user", BADGE_DEFINITIONS["first-code-run"])
    progress = progress_repository.get_progress("badge-user")

    assert len(progress.badges) == 1
    assert progress.badges[0].id == "first-code-run"
    assert progress.badges[0].title == "First Code Run"


def test_update_theme_unknown_user_returns_none():
    result = progress_repository.update_theme("ghost-user", "builder")
    assert result is None
