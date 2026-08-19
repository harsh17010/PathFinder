import networkx as nx
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import LearningPath, PathItem, CoursePrerequisite

class PathGeneratorService:
    async def generate_path(
        self, user_id: UUID, goal_id: UUID,
        recommended_courses: list[dict],
        db: AsyncSession
    ) -> LearningPath:
        
        course_ids = [c["course_id"] for c in recommended_courses]
        
        if not course_ids:
            path = LearningPath(user_id=user_id, goal_id=goal_id, status="generated")
            db.add(path)
            await db.commit()
            return path
            
        prereqs_res = await db.execute(
            select(CoursePrerequisite).where(CoursePrerequisite.course_id.in_(course_ids))
        )
        prereqs = prereqs_res.scalars().all()
        
        G = nx.DiGraph()
        for cid in course_ids:
            G.add_node(cid)
            
        for p in prereqs:
            if p.prerequisite_course_id in course_ids:
                G.add_edge(p.prerequisite_course_id, p.course_id)
                
        try:
            sorted_course_ids = list(nx.topological_sort(G))
        except nx.NetworkXUnfeasible:
            sorted_course_ids = course_ids
            
        milestones = self._chunk_into_milestones(sorted_course_ids, 4)
        
        path = LearningPath(user_id=user_id, goal_id=goal_id, status="generated")
        db.add(path)
        await db.commit()
        await db.refresh(path)
        
        seq = 1
        for m_idx, milestone in enumerate(milestones, start=1):
            for cid in milestone:
                status = "available" if m_idx == 1 else "locked"
                item = PathItem(
                    path_id=path.id,
                    course_id=cid,
                    sequence_order=seq,
                    milestone_number=m_idx,
                    status=status
                )
                db.add(item)
                seq += 1
                
        await db.commit()
        return path
    
    async def update_item_status(
        self, path_item_id: UUID, new_status: str, db: AsyncSession
    ) -> None:
        item_res = await db.execute(select(PathItem).where(PathItem.id == path_item_id))
        item = item_res.scalars().first()
        if not item: return
        
        item.status = new_status
        await db.commit()
        
        if new_status == "completed":
            milestone_items_res = await db.execute(
                select(PathItem).where(
                    PathItem.path_id == item.path_id,
                    PathItem.milestone_number == item.milestone_number
                )
            )
            milestone_items = milestone_items_res.scalars().all()
            if all(i.status == "completed" for i in milestone_items):
                next_milestone_res = await db.execute(
                    select(PathItem).where(
                        PathItem.path_id == item.path_id,
                        PathItem.milestone_number == item.milestone_number + 1
                    )
                )
                next_milestone_items = next_milestone_res.scalars().all()
                for nmi in next_milestone_items:
                    nmi.status = "available"
                await db.commit()
    
    def _chunk_into_milestones(self, sorted_courses: list, chunk_size: int = 4) -> list[list]:
        return [sorted_courses[i:i + chunk_size] for i in range(0, len(sorted_courses), chunk_size)]
    
    def _estimate_timeline(self, path_items: list, hours_per_week: float) -> dict:
        total_hours = sum(i.get("course_duration_hours", 0) or 0 for i in path_items)
        weeks = total_hours / hours_per_week if hours_per_week else 0
        return {"estimated_weeks": weeks, "total_hours": total_hours}
