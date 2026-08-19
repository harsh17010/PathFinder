from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class SkillBase(BaseModel):
    name: str
    track: Optional[str] = None
    description: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
