import pytest
from fastapi import HTTPException

from app.services.auth_service import auth_service


def test_register_creates_user():
    result = auth_service.register("test@example.com", "Test User", "secret123", "anon-auth-1")
    assert result["user"]["email"] == "test@example.com"
    assert result["user"]["name"] == "Test User"
    assert "token" in result


def test_register_rejects_duplicate_email():
    auth_service.register("dupe@example.com", "First", "secret123")
    with pytest.raises(HTTPException) as exc_info:
        auth_service.register("dupe@example.com", "Second", "secret456")
    assert exc_info.value.status_code == 409


def test_register_rejects_short_password():
    with pytest.raises(HTTPException) as exc_info:
        auth_service.register("short@example.com", "Short", "12345")
    assert exc_info.value.status_code == 400


def test_login_succeeds_with_correct_password():
    auth_service.register("login@example.com", "Login User", "mypassword")
    result = auth_service.login("login@example.com", "mypassword")
    assert result["user"]["email"] == "login@example.com"
    assert "token" in result


def test_login_fails_with_wrong_password():
    auth_service.register("wrong@example.com", "Wrong User", "correctpass")
    with pytest.raises(HTTPException) as exc_info:
        auth_service.login("wrong@example.com", "wrongpass")
    assert exc_info.value.status_code == 401


def test_get_current_user_from_token():
    result = auth_service.register("token@example.com", "Token User", "secret123")
    user = auth_service.get_current_user(result["token"])
    assert user["email"] == "token@example.com"


def test_progress_merges_on_register():
    from app.repositories.progress_repository import progress_repository

    progress_repository.complete_lesson("merge-anon", "lesson-print")
    progress_repository.complete_exercise("merge-anon", "exercise-print-hello")

    auth_service.register("merge@example.com", "Merge User", "secret123", "merge-anon")

    progress = progress_repository.get_progress("merge-anon")
    assert progress.xp == 40
    assert "lesson-print" in progress.completed_lessons
