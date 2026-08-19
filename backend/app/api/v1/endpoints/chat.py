from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_llm_service, get_embedding_service
from app.schemas.chat import ChatRequest, ChatResponse, ChatMessageCreate
from app.models.chat import ChatMessage
from app.models.learning_path import LearningPath, PathItem
from app.models.course import Course
from sqlalchemy import select
from uuid import uuid4
from app.services.profiling import ProfilingService
from app.services.explainability import ExplainabilityService

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest, 
    db: AsyncSession = Depends(get_db),
    embedding_service = Depends(get_embedding_service),
    llm_service = Depends(get_llm_service)
):
    session_id = request.session_id or uuid4()
    
    # Save user message
    user_msg = ChatMessage(user_id=request.user_id, session_id=session_id, role="user", content=request.message)
    db.add(user_msg)
    await db.commit()
    
    # Get user profile
    profiling = ProfilingService()
    profile = await profiling.get_user_profile_summary(request.user_id, db)
    
    # Get active path
    path_res = await db.execute(
        select(LearningPath).where(LearningPath.user_id == request.user_id, LearningPath.status == "generated")
    )
    active_path = path_res.scalars().first()
    
    path_items = []
    if active_path:
        items_res = await db.execute(
            select(PathItem, Course)
            .join(Course, PathItem.course_id == Course.id)
            .where(PathItem.path_id == active_path.id)
            .order_by(PathItem.sequence_order)
        )
        for pi, c in items_res.all():
            path_items.append({
                "course_title": c.title,
                "status": pi.status,
                "milestone": pi.milestone_number
            })
            
    # Answer using explainability service
    exp_service = ExplainabilityService()
    reply_text = await exp_service.answer_learner_question(request.message, profile, path_items, llm_service)
    
    # Save assistant message
    bot_msg = ChatMessage(user_id=request.user_id, session_id=session_id, role="assistant", content=reply_text)
    db.add(bot_msg)
    await db.commit()
    
    return ChatResponse(
        reply=reply_text,
        session_id=session_id,
        actions_taken=[]
    )
