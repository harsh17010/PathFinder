from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.core.database import get_db
from app.api.deps import get_embedding_service
from app.schemas.course import CourseResponse, CourseSearchResult, CourseSearchQuery
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
async def search_courses(
    payload: CourseSearchQuery, 
    db: AsyncSession = Depends(get_db),
    embedding_service = Depends(get_embedding_service)
):
    query_embedding = embedding_service.encode(payload.query)
    
    sql = text("""
        SELECT *, 1 - (embedding <=> :query_embedding::vector) as similarity_score
        FROM courses
        ORDER BY embedding <=> :query_embedding::vector
        LIMIT :limit
    """)
    
    result = await db.execute(sql, {
        "query_embedding": str(query_embedding),
        "limit": payload.limit
    })
    
    return result.all()
