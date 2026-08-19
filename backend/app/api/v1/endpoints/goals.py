from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.goal import GoalCreate, GoalResponse
from app.models.goal import Goal
from uuid import UUID
from typing import List

router = APIRouter()

@router.post("/", response_model=GoalResponse)
async def create_goal(goal: GoalCreate, db: AsyncSession = Depends(get_db)):
    db_goal = Goal(**goal.model_dump())
    db.add(db_goal)
    await db.commit()
    await db.refresh(db_goal)
    return db_goal

@router.get("/{user_id}", response_model=List[GoalResponse])
async def get_user_goals(user_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Goal).where(Goal.user_id == user_id))
    return result.scalars().all()
