from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.api.deps import get_llm_service
from app.schemas.goal import GoalCreate, GoalResponse, GoalParseRequest
from app.models.goal import Goal
from uuid import UUID
from typing import List
from app.services.profiling import ProfilingService

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

@router.post("/parse", response_model=GoalResponse)
async def parse_goal(
    req: GoalParseRequest, 
    db: AsyncSession = Depends(get_db),
    llm_service = Depends(get_llm_service)
):
    profiling = ProfilingService()
    parsed_goal = await profiling.parse_goal_with_llm(req.raw_text, llm_service, db)
    
    db_goal = Goal(
        user_id=req.user_id,
        raw_text=req.raw_text,
        target_role=parsed_goal.get("target_role"),
        target_skills=parsed_goal.get("target_skills"),
        timeframe_weeks=parsed_goal.get("timeframe_weeks"),
        hours_per_week=parsed_goal.get("hours_per_week"),
        status="active"
    )
    db.add(db_goal)
    await db.commit()
    await db.refresh(db_goal)
    return db_goal
