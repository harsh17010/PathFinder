from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, DateTime, ForeignKey, Integer, CheckConstraint
from app.core.database import Base

class LearningPath(Base):
    __tablename__ = "learning_paths"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    goal_id: Mapped[UUID] = mapped_column(ForeignKey("goals.id"))
    status: Mapped[str] = mapped_column(Text, default='active')
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class PathItem(Base):
    __tablename__ = "path_items"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    path_id: Mapped[UUID] = mapped_column(ForeignKey("learning_paths.id"))
    course_id: Mapped[UUID] = mapped_column(ForeignKey("courses.id"))
    sequence_order: Mapped[int] = mapped_column(Integer)
    milestone_number: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(Text, default='locked')
    explanation_text: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint("status IN ('locked', 'available', 'in_progress', 'completed')", name="check_path_item_status"),
    )
