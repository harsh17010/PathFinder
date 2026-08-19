from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.learning_path import LearningPathResponse, PathItemResponse
from app.models.learning_path import LearningPath, PathItem
from uuid import UUID
from typing import List

router = APIRouter()

@router.get("/{user_id}", response_model=List[LearningPathResponse])
async def get_user_paths(user_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LearningPath).where(LearningPath.user_id == user_id))
    return result.scalars().all()

@router.get("/{path_id}/items", response_model=List[PathItemResponse])
async def get_path_items(path_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PathItem).where(PathItem.path_id == path_id))
    return result.scalars().all()
