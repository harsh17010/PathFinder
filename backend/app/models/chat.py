from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, DateTime, ForeignKey, CheckConstraint
from app.core.database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    session_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))  # using user_id as proxy or separate table
    role: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("role IN ('user', 'assistant', 'tool')", name="check_chat_role"),
    )
