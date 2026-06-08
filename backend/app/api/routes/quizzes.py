from fastapi import APIRouter

from app.models.schemas import QuizSubmission
from app.services.quiz_service import quiz_service

router = APIRouter()


@router.get("/quizzes/{quiz_id}")
def get_quiz(quiz_id: str) -> dict:
    return quiz_service.get_quiz(quiz_id)


@router.post("/quizzes/{quiz_id}/submit")
def submit_quiz(quiz_id: str, submission: QuizSubmission) -> dict:
    return quiz_service.submit(quiz_id, submission.answers, submission.anonymous_user_id)
