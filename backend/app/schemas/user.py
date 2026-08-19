from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: Optional[str] = None
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
