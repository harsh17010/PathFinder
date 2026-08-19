from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_embedding_service
from pydantic import BaseModel
from uuid import UUID
from app.services.recommendation import RecommendationService

router = APIRouter()

class RecommendRequest(BaseModel):
    user_id: UUID
    goal_id: UUID
    limit: int = 20

@router.post("/generate")
async def generate_recommendations(
    req: RecommendRequest,
    db: AsyncSession = Depends(get_db),
    embedding_service = Depends(get_embedding_service)
):
    rec_service = RecommendationService()
    recs = await rec_service.get_recommendations(
        req.user_id, req.goal_id, db, embedding_service, req.limit
    )
    return {"recommendations": recs}
