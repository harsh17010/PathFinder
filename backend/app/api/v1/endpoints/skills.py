from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.core.database import get_db
from app.models import Skill
from app.schemas.skill import SkillResponse

router = APIRouter()

@router.get("/", response_model=List[SkillResponse])
async def get_skills(track: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    query = select(Skill)
    if track:
        query = query.where(Skill.track == track)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/tracks", response_model=List[str])
async def get_tracks(db: AsyncSession = Depends(get_db)):
    query = select(Skill.track).distinct().where(Skill.track != None)
    result = await db.execute(query)
    return [r[0] for r in result.all()]
