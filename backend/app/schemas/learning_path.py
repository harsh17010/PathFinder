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

class PathGenerateRequest(BaseModel):
    user_id: UUID
    goal_id: UUID

class PathItemDetail(BaseModel):
    id: UUID
    course_id: UUID
    course_title: str
    course_description: str
    course_provider: str | None = None
    course_track: str | None = None
    course_difficulty: str | None = None
    course_duration_hours: float | None = None
    course_rating: float | None = None
    sequence_order: int
    milestone_number: int | None = None
    status: str
    explanation_text: str | None = None
    model_config = ConfigDict(from_attributes=True)

class LearningPathDetail(BaseModel):
    id: UUID
    user_id: UUID
    goal_id: UUID
    status: str
    generated_at: datetime
    items: list[PathItemDetail] = []
    overview_explanation: str | None = None
    estimated_weeks: float | None = None
    model_config = ConfigDict(from_attributes=True)

