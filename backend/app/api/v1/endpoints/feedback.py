from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.models.feedback import FeedbackEvent

router = APIRouter()

@router.post("/", response_model=FeedbackResponse)
async def create_feedback(feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    db_feedback = FeedbackEvent(**feedback.model_dump())
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback
