from fastapi import APIRouter
from app.api.v1.endpoints import users, courses, goals, recommendations, paths, chat, feedback, skills

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(paths.router, prefix="/paths", tags=["paths"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
api_router.include_router(skills.router, prefix="/skills", tags=["skills"])
