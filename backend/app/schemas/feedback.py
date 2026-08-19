from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class FeedbackCreate(BaseModel):
    user_id: UUID
    path_item_id: UUID
    feedback_type: str

class FeedbackResponse(FeedbackCreate):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PathItemStatusUpdate(BaseModel):
    status: str

