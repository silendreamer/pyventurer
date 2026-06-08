from app.db.seed_curriculum import seed_curriculum
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
    assert first_module["title"] == "Welcome to Python"
    assert first_module["lessons"][0]["title"] == "What is Python?"
    assert first_module["lessons"][3]["id"] == "lesson-your-first-python-program"
    assert first_module["lessons"][3]["implemented"] is True
    assert first_module["projects"][0]["title"] == "Run your first Python program"


def test_curriculum_seed_is_idempotent():
    seed_curriculum(content_service.repository.connection)
    seed_curriculum(content_service.repository.connection)

    lesson_count = content_service.repository.connection.execute("SELECT COUNT(*) FROM lessons").fetchone()[0]
    module_count = content_service.repository.connection.execute("SELECT COUNT(*) FROM modules").fetchone()[0]

    assert module_count == 15
    assert lesson_count == 77


def test_python_courses_exist_with_intermediate_placeholder():
    catalog = content_service.get_catalog()
    courses = {course.slug: course for course in catalog["courses"]}

    assert "python-for-beginners" in courses
    assert courses["python-for-beginners"].status == "published"
    assert "python-for-intermediate-users" in courses
    assert courses["python-for-intermediate-users"].status == "coming_soon"


def test_course_outline_returns_modules_in_order():
    outline = content_service.get_course_outline("python-for-beginners")
    module_titles = [module["title"] for module in outline["modules"]]

    assert module_titles[0] == "Welcome to Python"
    assert module_titles[1] == "Printing and Comments"
    assert module_titles[-1] == "Beginner Projects"
    assert outline["next_course"]["slug"] == "python-for-intermediate-users"


def test_quiz_api_hides_correct_answers():
    quiz = quiz_service.get_quiz("quiz-print-basics")

    assert "correct_choice" not in quiz["questions"][0]
    assert "explanation" not in quiz["questions"][0]
    assert len(quiz["questions"]) == 3


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
        {"q1": "Shows output", "q2": 'print("Hello World")', "q3": "#"},
        "test-quiz-user",
    )

    assert result["score"] == 100
    assert result["passed"] is True


def test_theme_resolution_defaults_to_explorer():
    theme = theme_service.resolve_for_user("unknown-user")

    assert theme.id == "explorer"
    assert theme.tokens.primary
