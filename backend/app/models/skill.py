from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text
from app.core.database import Base

class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(Text, unique=True)
    track: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
