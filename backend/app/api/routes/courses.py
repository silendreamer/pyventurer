from fastapi import APIRouter

from app.services.content_service import content_service

router = APIRouter()


@router.get("/catalog")
def get_catalog() -> dict:
    return content_service.get_catalog()


@router.get("/courses/{course_slug}")
def get_course(course_slug: str) -> dict:
    return content_service.get_course_overview(course_slug)
