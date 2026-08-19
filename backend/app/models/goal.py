from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, DateTime, ForeignKey, Numeric, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base

class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    raw_text: Mapped[str | None] = mapped_column(Text)
    target_role: Mapped[str | None] = mapped_column(Text)
    target_skills: Mapped[dict | None] = mapped_column(JSONB)
    timeframe_weeks: Mapped[int | None] = mapped_column(Integer)
    hours_per_week: Mapped[float | None] = mapped_column(Numeric)
    status: Mapped[str] = mapped_column(Text, default='active')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("status IN ('active', 'completed', 'abandoned')", name="check_goal_status"),
    )
