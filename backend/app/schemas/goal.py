from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, Dict, Any
from datetime import datetime

class GoalBase(BaseModel):
    raw_text: Optional[str] = None
    target_role: Optional[str] = None
    target_skills: Optional[Dict[str, Any]] = None
    timeframe_weeks: Optional[int] = None
    hours_per_week: Optional[float] = None
    status: str = "active"

class GoalCreate(GoalBase):
    user_id: UUID

class GoalResponse(GoalBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
