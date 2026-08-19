from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_llm_service
from app.schemas.user import UserCreate, UserResponse, UserProfileResponse, OnboardingRequest
from app.models.user import User, UserSkill, UserInterest
from app.models.skill import Skill
from app.models.goal import Goal
from sqlalchemy import select
from uuid import UUID
from app.services.profiling import ProfilingService

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    db_user = await db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/onboard")
async def onboard_user(req: OnboardingRequest, db: AsyncSession = Depends(get_db), llm_service = Depends(get_llm_service)):
    # 1. Create User
    user = User(name=req.name, email=req.email)
    db.add(user)
    await db.flush()
    
    # 2. Add Skills
    for s in req.skills:
        skill_res = await db.execute(select(Skill).where(Skill.name == s.get("skill_name")))
        skill = skill_res.scalars().first()
        if skill:
            db.add(UserSkill(user_id=user.id, skill_id=skill.id, proficiency_level=s.get("proficiency_level", 0)))
            
    # 3. Add Interests
    for track in req.interests:
        db.add(UserInterest(user_id=user.id, track=track, weight=1.0))
        
    await db.commit()
    
    # 4. Parse Goal
    profiling = ProfilingService()
    parsed_goal = await profiling.parse_goal_with_llm(req.goal_text, llm_service, db)
    goal = Goal(
        user_id=user.id,
        raw_text=req.goal_text,
        target_role=parsed_goal.get("target_role"),
        target_skills=parsed_goal.get("target_skills"),
        timeframe_weeks=parsed_goal.get("timeframe_weeks"),
        hours_per_week=parsed_goal.get("hours_per_week"),
        status="active"
    )
    db.add(goal)
    await db.commit()
    await db.refresh(user)
    
    return {"user_id": user.id, "message": "Onboarding complete"}

@router.get("/{user_id}/profile", response_model=UserProfileResponse)
async def get_profile(user_id: UUID, db: AsyncSession = Depends(get_db)):
    profiling = ProfilingService()
    profile = await profiling.get_user_profile_summary(user_id, db)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return profile
