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

class UserProfileResponse(BaseModel):
    id: UUID
    name: str | None = None
    email: str
    created_at: datetime
    skills: list[dict] = []
    interests: list[dict] = []
    goals: list[dict] = []
    completed_courses: list[dict] = []
    model_config = ConfigDict(from_attributes=True)

class OnboardingRequest(BaseModel):
    name: str
    email: str
    skills: list[dict] = []
    interests: list[str] = []
    goal_text: str

