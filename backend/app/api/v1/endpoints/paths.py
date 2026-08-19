from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.api.deps import get_embedding_service, get_llm_service
from app.schemas.learning_path import LearningPathResponse, PathItemResponse, PathGenerateRequest, LearningPathDetail
from app.schemas.feedback import PathItemStatusUpdate
from app.models.learning_path import LearningPath, PathItem
from app.models.course import Course
from app.models.goal import Goal
from uuid import UUID
from typing import List
from app.services.recommendation import RecommendationService
from app.services.path_generator import PathGeneratorService
from app.services.explainability import ExplainabilityService

router = APIRouter()

@router.get("/{user_id}", response_model=List[LearningPathResponse])
async def get_user_paths(user_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LearningPath).where(LearningPath.user_id == user_id))
    return result.scalars().all()

@router.get("/{path_id}/items", response_model=List[PathItemResponse])
async def get_path_items(path_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PathItem).where(PathItem.path_id == path_id))
    return result.scalars().all()

@router.post("/generate", response_model=LearningPathResponse)
async def generate_path(
    req: PathGenerateRequest, 
    db: AsyncSession = Depends(get_db),
    embedding_service = Depends(get_embedding_service)
):
    rec_service = RecommendationService()
    recs = await rec_service.get_recommendations(req.user_id, req.goal_id, db, embedding_service, 20)
    
    path_service = PathGeneratorService()
    path = await path_service.generate_path(req.user_id, req.goal_id, recs, db)
    
    return path

@router.get("/{path_id}/detail", response_model=LearningPathDetail)
async def get_path_detail(
    path_id: UUID, 
    db: AsyncSession = Depends(get_db),
    llm_service = Depends(get_llm_service)
):
    path_res = await db.execute(select(LearningPath).where(LearningPath.id == path_id))
    path = path_res.scalars().first()
    if not path:
        raise HTTPException(status_code=404, detail="Path not found")
        
    items_res = await db.execute(select(PathItem, Course).join(Course, PathItem.course_id == Course.id).where(PathItem.path_id == path_id).order_by(PathItem.sequence_order))
    items_data = items_res.all()
    
    items = []
    for pi, c in items_data:
        items.append({
            "id": pi.id,
            "course_id": c.id,
            "course_title": c.title,
            "course_description": c.description,
            "course_provider": c.provider,
            "course_track": c.track,
            "course_difficulty": c.difficulty_level,
            "course_duration_hours": c.duration_hours,
            "course_rating": c.rating,
            "sequence_order": pi.sequence_order,
            "milestone_number": pi.milestone_number,
            "status": pi.status,
            "explanation_text": pi.explanation_text
        })
        
    path_service = PathGeneratorService()
    timeline = path_service._estimate_timeline(items, 10.0) # Assume 10 hours/week for now
    
    # Optional: Get explanation
    goal_res = await db.execute(select(Goal).where(Goal.id == path.goal_id))
    goal = goal_res.scalars().first()
    
    overview = None
    if goal:
        exp_service = ExplainabilityService()
        overview = await exp_service.explain_path_overview(items, goal, llm_service)
        
    return {
        "id": path.id,
        "user_id": path.user_id,
        "goal_id": path.goal_id,
        "status": path.status,
        "generated_at": path.generated_at,
        "items": items,
        "overview_explanation": overview,
        "estimated_weeks": timeline.get("estimated_weeks")
    }

@router.patch("/items/{item_id}/status")
async def update_item_status(
    item_id: UUID, 
    req: PathItemStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    path_service = PathGeneratorService()
    await path_service.update_item_status(item_id, req.status, db)
    return {"message": "Status updated"}
