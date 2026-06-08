from fastapi import APIRouter

from app.models.schemas import ExerciseSubmission
from app.services.exercise_service import exercise_service

router = APIRouter()


@router.get("/exercises/{exercise_id}")
def get_exercise(exercise_id: str) -> dict:
    return exercise_service.get_exercise(exercise_id)


@router.post("/exercises/{exercise_id}/submit")
def submit_exercise(exercise_id: str, submission: ExerciseSubmission) -> dict:
    return exercise_service.submit(exercise_id, submission.code, submission.anonymous_user_id)
