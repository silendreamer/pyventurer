from fastapi import APIRouter

from app.services.content_service import content_service

router = APIRouter()


@router.get("/catalog")
def get_catalog() -> dict:
    return content_service.get_catalog()


@router.get("/curriculum")
def get_curriculum() -> dict:
    return content_service.get_curriculum_tree()


@router.get("/languages")
def get_languages() -> dict:
    return {"languages": content_service.get_catalog()["languages"]}


@router.get("/courses")
def get_courses() -> dict:
    return {"courses": content_service.get_catalog()["courses"]}


@router.get("/lessons/{lesson_id}")
def get_lesson_bundle(lesson_id: str) -> dict:
    return content_service.get_lesson_bundle(lesson_id)


@router.get("/projects/{project_slug}")
def get_project(project_slug: str) -> dict:
    return content_service.get_project(project_slug)


@router.get("/courses/{course_slug}/outline")
def get_course_outline(course_slug: str) -> dict:
    return content_service.get_course_outline(course_slug)


@router.get("/courses/{course_slug}/completion")
def get_course_completion(course_slug: str) -> dict:
    return content_service.get_course_completion(course_slug)


@router.get("/courses/{course_slug}")
def get_course(course_slug: str) -> dict:
    return content_service.get_course_overview(course_slug)
