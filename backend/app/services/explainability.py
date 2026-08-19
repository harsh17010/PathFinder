from app.models import Course, Goal
from app.services.llm import LLMService

class ExplainabilityService:
    async def explain_recommendation(
        self, course: Course, user_profile: dict, goal: Goal,
        skill_gap: list[dict], llm_service: LLMService
    ) -> str:
        system_prompt = "You are a learning path advisor. Explain concisely why a course is recommended based on data."
        
        prompt = f"""
Course: {course.title}
Difficulty: {course.difficulty_level}
Duration: {course.duration_hours} hours

User Current Profile:
Skills: {user_profile.get("skills")}

Goal:
Target Role: {goal.target_role}

Skill Gap it fills:
{skill_gap}

Explain in 2-3 sentences WHY this specific course fits the user's goal.
"""
        try:
            explanation = await llm_service.generate(prompt, system_prompt)
        except Exception:
            explanation = f"This course fits your goal of becoming a {goal.target_role}."
        return explanation

    async def explain_path_overview(
        self, path_items: list, goal: Goal, llm_service: LLMService
    ) -> str:
        system_prompt = "You are an AI advisor. Give a brief overview of the learning path."
        
        course_list = [item.get("course_title", "Course") for item in path_items]
        
        prompt = f"""
Goal: {goal.target_role}
Path Courses: {course_list}

Provide an overview of this learning path in 2-3 sentences, explaining why these milestones make sense.
"""
        try:
            explanation = await llm_service.generate(prompt, system_prompt)
        except Exception:
            explanation = "This path will guide you through the necessary steps to achieve your learning goal."
        return explanation

    async def answer_learner_question(
        self, question: str, user_profile: dict, path_items: list,
        llm_service: LLMService
    ) -> str:
        system_prompt = "You are a helpful learning path advisor answering a learner's question."
        
        course_list = [item.get("course_title", "Course") for item in path_items]
        prompt = f"""
User Profile: {user_profile}
Path Courses: {course_list}

User Question: {question}

Answer directly and concisely based on the user's profile and path data.
"""
        try:
            answer = await llm_service.generate(prompt, system_prompt)
        except Exception:
            answer = "I'm sorry, I can't answer that right now."
        return answer
