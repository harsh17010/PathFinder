from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.models import Goal, FeedbackEvent, PathItem, Course, LearningPath
from app.core.embeddings import EmbeddingService
from app.services.profiling import ProfilingService

class RecommendationService:
    async def get_recommendations(
        self, user_id: UUID, goal_id: UUID, 
        db: AsyncSession, embedding_service: EmbeddingService,
        limit: int = 20
    ) -> list[dict]:
        goal_res = await db.execute(select(Goal).where(Goal.id == goal_id, Goal.user_id == user_id))
        goal = goal_res.scalars().first()
        if not goal:
            return []
            
        profiling_service = ProfilingService()
        skill_gap = await profiling_service.compute_skill_gap(user_id, goal, db)
        
        gap_text = " ".join([f"Needs {g['skill_name']} at level {g['target_level']} from current level {g['current_level']}." for g in skill_gap])
        if not gap_text:
            gap_text = "General learning"
            
        query_embedding = embedding_service.encode(gap_text)
        
        sql = text("""
            SELECT c.*, 1 - (c.embedding <=> :query_embedding::vector) as similarity
            FROM courses c
            WHERE c.id NOT IN (SELECT course_id FROM completed_courses WHERE user_id = :user_id)
            ORDER BY c.embedding <=> :query_embedding::vector
            LIMIT :limit
        """)
        
        result = await db.execute(sql, {
            "query_embedding": str(query_embedding),
            "user_id": user_id,
            "limit": limit * 2
        })
        
        courses = result.all()
        
        recommended = []
        for c in courses:
            gap_coverage = 0.5
            score = (c.similarity * 0.5) + (gap_coverage * 0.3) + ((c.rating / 5.0) * 0.2)
            recommended.append({
                "course_id": c.id,
                "course_title": c.title,
                "course_description": c.description,
                "course_provider": c.provider,
                "course_track": c.track,
                "course_difficulty": c.difficulty_level,
                "course_duration_hours": c.duration_hours,
                "course_rating": c.rating,
                "similarity": c.similarity,
                "score": score
            })
            
        recommended.sort(key=lambda x: x["score"], reverse=True)
        return recommended[:limit]

    async def rerank_after_feedback(
        self, path_id: UUID, feedback_event: FeedbackEvent,
        db: AsyncSession, embedding_service: EmbeddingService
    ) -> None:
        # Simple implementation for re-ranking
        # We would typically adjust weights or user embedding and re-sort available items
        items_res = await db.execute(
            select(PathItem).where(
                PathItem.path_id == path_id,
                PathItem.status.in_(["available", "locked"])
            ).order_by(PathItem.sequence_order)
        )
        items = items_res.scalars().all()
        
        # Example re-rank logic based on feedback type:
        if feedback_event.feedback_type in ["too_easy", "too_hard", "not_relevant"]:
            # Reverse order of remaining as a dummy action, or just shuffle
            # For a real implementation, we'd query Course properties and adjust
            pass
