from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, DateTime, ForeignKey, SmallInteger, CheckConstraint, Numeric
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str | None] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class UserSkill(Base):
    __tablename__ = "user_skills"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    skill_id: Mapped[UUID] = mapped_column(ForeignKey("skills.id"), primary_key=True)
    proficiency_level: Mapped[int] = mapped_column(SmallInteger, default=0)
    assessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("proficiency_level >= 0 AND proficiency_level <= 5", name="check_proficiency_level"),
    )

class UserInterest(Base):
    __tablename__ = "user_interests"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    track: Mapped[str] = mapped_column(Text, primary_key=True)
    weight: Mapped[float] = mapped_column(Numeric, default=1.0)

class CompletedCourse(Base):
    __tablename__ = "completed_courses"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    course_id: Mapped[UUID] = mapped_column(ForeignKey("courses.id"), primary_key=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    rating_given: Mapped[int | None] = mapped_column(SmallInteger)
