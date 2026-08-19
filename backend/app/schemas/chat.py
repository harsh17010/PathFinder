from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class ChatMessageCreate(BaseModel):
    user_id: UUID
    session_id: Optional[UUID] = None
    role: str
    content: str

class ChatMessageResponse(ChatMessageCreate):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ChatRequest(BaseModel):
    user_id: UUID
    message: str
    session_id: Optional[UUID] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: UUID
    actions_taken: list[str] = []

