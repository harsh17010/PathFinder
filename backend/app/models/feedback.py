from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, DateTime, ForeignKey, CheckConstraint
from app.core.database import Base

class FeedbackEvent(Base):
    __tablename__ = "feedback_events"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    path_item_id: Mapped[UUID] = mapped_column(ForeignKey("path_items.id"))
    feedback_type: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("feedback_type IN ('too_easy', 'too_hard', 'not_relevant', 'helpful')", name="check_feedback_type"),
    )
