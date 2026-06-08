from fastapi import APIRouter, Depends, Response

from app.auth import get_current_user
from app.models.schemas import LoginRequest, RegisterRequest
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth")


@router.post("/register")
def register(request: RegisterRequest, response: Response) -> dict:
    result = auth_service.register(
        email=request.email,
        name=request.name,
        password=request.password,
        anonymous_user_id=request.anonymous_user_id,
    )
    response.set_cookie(
        key="session_token",
        value=result["token"],
        httponly=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
    )
    return {"user": result["user"], "message": "Account created. Progress saved."}


@router.post("/login")
def login(request: LoginRequest, response: Response) -> dict:
    result = auth_service.login(email=request.email, password=request.password)
    response.set_cookie(
        key="session_token",
        value=result["token"],
        httponly=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
    )
    return {"user": result["user"]}


@router.post("/logout")
def logout(response: Response) -> dict:
    response.delete_cookie(key="session_token")
    return {"message": "Logged out"}


@router.get("/me")
def me(user: dict = Depends(get_current_user)) -> dict:
    return {"user": user}
