from pydantic import BaseModel

from app.models.domain import LearnerProfile


class ProfileRequest(BaseModel):
    profile: LearnerProfile
    anonymous_user_id: str = "demo-user"


class PlacementSubmission(BaseModel):
    anonymous_user_id: str = "demo-user"
    answers: dict[str, str]


class ExerciseSubmission(BaseModel):
    anonymous_user_id: str = "demo-user"
    code: str


class QuizSubmission(BaseModel):
    anonymous_user_id: str = "demo-user"
    answers: dict[str, str]


class ThemeSelection(BaseModel):
    anonymous_user_id: str = "demo-user"
    theme_id: str


class AccountRequest(BaseModel):
    anonymous_user_id: str = "demo-user"
    email: str
    name: str
