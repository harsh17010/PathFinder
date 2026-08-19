from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    provider: Optional[str] = None
    track: Optional[str] = None
    difficulty_level: Optional[str] = None
    duration_hours: Optional[float] = None
    rating: float = 4.0
    url: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CourseSearchResult(CourseResponse):
    similarity_score: float

class CourseSearchQuery(BaseModel):
    query: str
    user_id: Optional[UUID] = None
    limit: int = 10

