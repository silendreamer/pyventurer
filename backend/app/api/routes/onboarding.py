from fastapi import APIRouter

from app.models.schemas import AccountRequest, ProfileRequest
from app.repositories.progress_repository import progress_repository
from app.services.account_service import account_service
from app.services.recommendation_service import recommendation_service
from app.services.theme_service import theme_service

router = APIRouter()


@router.post("/onboarding/profile")
def save_profile(request: ProfileRequest) -> dict:
    profile = progress_repository.save_profile(request.anonymous_user_id, request.profile)
    theme = theme_service.resolve_for_user(request.anonymous_user_id)
    recommendations = recommendation_service.recommend(profile)
    return {"profile": profile, "theme": theme, "recommendations": recommendations}


@router.post("/account")
def create_account(request: AccountRequest) -> dict:
    return account_service.create_placeholder_account(request.anonymous_user_id, request.email, request.name)
