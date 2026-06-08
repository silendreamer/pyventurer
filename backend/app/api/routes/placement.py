from fastapi import APIRouter

from app.models.schemas import PlacementSubmission
from app.services.placement_service import placement_service

router = APIRouter()


@router.get("/courses/{course_id}/placement")
def get_placement(course_id: str) -> dict:
    return placement_service.get_assessment(course_id)


@router.post("/courses/{course_id}/placement")
def submit_placement(course_id: str, submission: PlacementSubmission) -> dict:
    return placement_service.grade(course_id, submission.answers, submission.anonymous_user_id)
