from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime

class PathItemResponse(BaseModel):
    id: UUID
    path_id: UUID
    course_id: UUID
    sequence_order: int
    milestone_number: Optional[int] = None
    status: str
    explanation_text: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class LearningPathResponse(BaseModel):
    id: UUID
    user_id: UUID
    goal_id: UUID
    status: str
    generated_at: datetime
    model_config = ConfigDict(from_attributes=True)
