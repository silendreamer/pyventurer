from fastapi import Cookie, HTTPException

from app.services.auth_service import auth_service


def get_current_user(session_token: str | None = Cookie(default=None)) -> dict:
    if session_token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return auth_service.get_current_user(session_token)


def get_optional_user(session_token: str | None = Cookie(default=None)) -> dict | None:
    if session_token is None:
        return None
    try:
        return auth_service.get_current_user(session_token)
    except HTTPException:
        return None
