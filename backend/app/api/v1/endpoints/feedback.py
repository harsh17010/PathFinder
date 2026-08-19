from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.api.deps import get_embedding_service
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.models.feedback import FeedbackEvent
from app.models.learning_path import PathItem
from app.services.recommendation import RecommendationService

router = APIRouter()

@router.post("/", response_model=FeedbackResponse)
async def create_feedback(
    feedback: FeedbackCreate, 
    db: AsyncSession = Depends(get_db),
    embedding_service = Depends(get_embedding_service)
):
    db_feedback = FeedbackEvent(**feedback.model_dump())
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    
    # Trigger re-ranking
    path_item_res = await db.execute(select(PathItem).where(PathItem.id == feedback.path_item_id))
    path_item = path_item_res.scalars().first()
    
    if path_item:
        rec_service = RecommendationService()
        await rec_service.rerank_after_feedback(path_item.path_id, db_feedback, db, embedding_service)
        
    return db_feedback
