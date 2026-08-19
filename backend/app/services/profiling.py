import json
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Goal, User, UserSkill, UserInterest, CompletedCourse, Skill, Course
from app.services.llm import LLMService

class ProfilingService:
    async def parse_goal_with_llm(self, raw_text: str, llm_service: LLMService, db: AsyncSession) -> dict:
        result = await db.execute(select(Skill.name))
        skill_names = [row[0] for row in result.all()]
        
        system_prompt = "You are a learning path advisor. Extract structured information from the learner's goal. Return ONLY valid JSON."
        prompt = f"Given this goal: '{raw_text}', extract: target_role (string), target_skills (array of strings from this list: {skill_names}), timeframe_weeks (integer), hours_per_week (float). Respond ONLY with valid JSON."
        
        try:
            response = await llm_service.generate(prompt, system_prompt)
            parsed = json.loads(response)
        except Exception:
            parsed = {
                "target_role": "Learner",
                "target_skills": [],
                "timeframe_weeks": 12,
                "hours_per_week": 5.0
            }
        return parsed

    async def compute_skill_gap(self, user_id: UUID, goal: Goal, db: AsyncSession) -> list[dict]:
        if not goal.target_skills:
            return []
            
        result = await db.execute(select(UserSkill).where(UserSkill.user_id == user_id))
        user_skills_db = result.scalars().all()
        
        skill_ids = [us.skill_id for us in user_skills_db]
        skills_map = {}
        if skill_ids:
            skills_res = await db.execute(select(Skill).where(Skill.id.in_(skill_ids)))
            for sk in skills_res.scalars().all():
                skills_map[sk.id] = sk.name
                
        current_skills = {skills_map.get(us.skill_id): us.proficiency_level for us in user_skills_db if us.skill_id in skills_map}
        
        gap = []
        target_skills = goal.target_skills if isinstance(goal.target_skills, list) else list(goal.target_skills.keys()) if isinstance(goal.target_skills, dict) else []
        for skill in target_skills:
            if isinstance(skill, dict):
                skill_name = skill.get("skill_name")
            else:
                skill_name = str(skill)
            
            if not skill_name: continue
            
            current_lvl = current_skills.get(skill_name, 0)
            target_lvl = 3 # default target level
            if isinstance(goal.target_skills, dict) and skill_name in goal.target_skills:
                try:
                    target_lvl = int(goal.target_skills[skill_name])
                except:
                    pass
            
            if current_lvl < target_lvl:
                gap.append({
                    "skill_name": skill_name,
                    "current_level": current_lvl,
                    "target_level": target_lvl,
                    "gap": target_lvl - current_lvl
                })
        return gap

    async def get_user_profile_summary(self, user_id: UUID, db: AsyncSession) -> dict:
        user_res = await db.execute(select(User).where(User.id == user_id))
        user = user_res.scalars().first()
        if not user:
            return {}
            
        uskill_res = await db.execute(select(UserSkill, Skill).join(Skill, UserSkill.skill_id == Skill.id).where(UserSkill.user_id == user_id))
        skills = [{"skill_name": sk.name, "track": sk.track, "proficiency_level": us.proficiency_level} for us, sk in uskill_res.all()]
        
        uint_res = await db.execute(select(UserInterest).where(UserInterest.user_id == user_id))
        interests = [{"track": ui.track, "weight": ui.weight} for ui in uint_res.scalars().all()]
        
        goals_res = await db.execute(select(Goal).where(Goal.user_id == user_id, Goal.status == "active"))
        goals = [{"id": str(g.id), "target_role": g.target_role, "target_skills": g.target_skills} for g in goals_res.scalars().all()]
        
        cc_res = await db.execute(select(CompletedCourse, Course).join(Course, CompletedCourse.course_id == Course.id).where(CompletedCourse.user_id == user_id))
        completed = [{"course_title": c.title, "completed_at": cc.completed_at.isoformat()} for cc, c in cc_res.all()]
        
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
            "skills": skills,
            "interests": interests,
            "goals": goals,
            "completed_courses": completed
        }
