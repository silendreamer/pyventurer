from fastapi import APIRouter

from app.services.content_service import content_service

router = APIRouter()


@router.get("/catalog")
def get_catalog() -> dict:
    return content_service.get_catalog()


@router.get("/curriculum")
def get_curriculum() -> dict:
    return content_service.get_curriculum_tree()


@router.get("/lessons/{lesson_id}")
def get_lesson_bundle(lesson_id: str) -> dict:
    return content_service.get_lesson_bundle(lesson_id)


@router.get("/courses/{course_slug}")
def get_course(course_slug: str) -> dict:
    return content_service.get_course_overview(course_slug)
