from app.models.domain import LearnerProfile
from app.services.content_service import content_service
from app.services.exercise_service import exercise_service
from app.services.placement_service import placement_service
from app.services.quiz_service import quiz_service
from app.services.recommendation_service import recommendation_service
from app.services.theme_service import theme_service


def test_recommendation_uses_profile_goal():
    profile = LearnerProfile(
        age_range="teen-adult",
        experience_level="new",
        learning_goal="ai",
        motivation_type="create-real-projects",
        preferred_style="guided",
        selected_theme_id="explorer",
    )

    recommendations = recommendation_service.recommend(profile)

    assert recommendations[0].course.id == "python-demo"
    assert recommendations[0].starting_lesson_id == "lesson-print"


def test_curriculum_tree_exposes_course_module_lesson_hierarchy():
    curriculum = content_service.get_curriculum_tree()
    python = curriculum["languages"][0]
    beginner_course = python["courses"][0]
    first_module = beginner_course["modules"][0]

    assert python["title"] == "Python"
    assert beginner_course["title"] == "Python for Beginners"
    assert first_module["title"] == "Python Basics"
    assert first_module["lessons"][0]["id"] == "lesson-print"
    assert first_module["lessons"][0]["implemented"] is True
    assert first_module["lessons"][1]["id"] == "lesson-variables"
    assert first_module["lessons"][1]["implemented"] is True
    assert first_module["lessons"][2]["implemented"] is False


def test_placement_scores_on_backend():
    result = placement_service.grade(
        "python-demo",
        {"p1": "A little", "p2": "Hi", "p3": "variables"},
        "test-placement-user",
    )

    assert result["score"] == 100
    assert result["passed"] is True


def test_exercise_grades_real_python_output():
    result = exercise_service.submit("exercise-print-hello", 'print("Hello World")', "test-exercise-user")

    assert result["passed"] is True
    assert result["output"] == "Hello World"
    assert any(badge.id == "first-code-run" for badge in result["progress"].badges)


def test_exercise_blocks_dangerous_code():
    result = exercise_service.submit("exercise-print-hello", 'import os\nprint("Hello World")', "test-danger-user")

    assert result["passed"] is False
    assert "blocks imports" in result["message"]


def test_quiz_does_not_need_frontend_answers():
    result = quiz_service.submit(
        "quiz-print-basics",
        {"q1": "Shows output", "q2": 'print("Hello World")'},
        "test-quiz-user",
    )

    assert result["score"] == 100
    assert result["passed"] is True


def test_theme_resolution_defaults_to_explorer():
    theme = theme_service.resolve_for_user("unknown-user")

    assert theme.id == "explorer"
    assert theme.tokens.primary
