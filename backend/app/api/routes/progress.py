from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.services.progress_service import progress_service

router = APIRouter()


@router.get("/progress/me")
def get_my_progress(user: dict = Depends(get_current_user)):
    return progress_service.get_progress_for_user(user["id"])


@router.get("/progress/{anonymous_user_id}")
def get_progress(anonymous_user_id: str):
    return progress_service.get_progress(anonymous_user_id)


@router.post("/progress/{anonymous_user_id}/lessons/{lesson_id}/complete")
def complete_lesson(anonymous_user_id: str, lesson_id: str):
    return progress_service.complete_lesson(anonymous_user_id, lesson_id)
