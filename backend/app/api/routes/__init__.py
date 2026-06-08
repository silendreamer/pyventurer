from fastapi import APIRouter

from app.api.routes import auth, courses, exercises, onboarding, placement, progress, quizzes, themes

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(onboarding.router, tags=["onboarding"])
api_router.include_router(courses.router, tags=["courses"])
api_router.include_router(placement.router, tags=["placement"])
api_router.include_router(exercises.router, tags=["exercises"])
api_router.include_router(quizzes.router, tags=["quizzes"])
api_router.include_router(progress.router, tags=["progress"])
api_router.include_router(themes.router, tags=["themes"])
