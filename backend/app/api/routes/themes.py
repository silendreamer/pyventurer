from fastapi import APIRouter

from app.models.schemas import ThemeSelection
from app.services.theme_service import theme_service

router = APIRouter()


@router.get("/themes")
def list_themes() -> dict:
    return {"themes": theme_service.list_themes()}


@router.get("/themes/current/{anonymous_user_id}")
def current_theme(anonymous_user_id: str):
    return theme_service.resolve_for_user(anonymous_user_id)


@router.post("/themes/select")
def select_theme(selection: ThemeSelection):
    return theme_service.select_theme(selection.anonymous_user_id, selection.theme_id)
