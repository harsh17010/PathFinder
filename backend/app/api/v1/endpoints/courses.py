from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.course import CourseResponse, CourseSearchResult
from app.models.course import Course
from uuid import UUID
from typing import List

router = APIRouter()

@router.get("/", response_model=List[CourseResponse])
async def list_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).limit(10))
    return result.scalars().all()

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: UUID, db: AsyncSession = Depends(get_db)):
    db_course = await db.get(Course, course_id)
    return db_course

@router.post("/search", response_model=List[CourseSearchResult])
async def search_courses(query: str, db: AsyncSession = Depends(get_db)):
    # Stub implementation for similarity search
    return []
