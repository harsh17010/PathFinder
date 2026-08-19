from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Numeric, CheckConstraint, SmallInteger, ForeignKey, DateTime
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    provider: Mapped[str | None] = mapped_column(Text)
    track: Mapped[str | None] = mapped_column(Text)
    difficulty_level: Mapped[str | None] = mapped_column(Text)
    duration_hours: Mapped[float | None] = mapped_column(Numeric)
    rating: Mapped[float | None] = mapped_column(Numeric, default=4.0)
    url: Mapped[str | None] = mapped_column(Text)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(384))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("difficulty_level IN ('beginner', 'intermediate', 'advanced')", name="check_difficulty_level"),
    )

class CourseSkill(Base):
    __tablename__ = "course_skills"

    course_id: Mapped[UUID] = mapped_column(ForeignKey("courses.id"), primary_key=True)
    skill_id: Mapped[UUID] = mapped_column(ForeignKey("skills.id"), primary_key=True)
    proficiency_gained: Mapped[int] = mapped_column(SmallInteger, default=1)

class CoursePrerequisite(Base):
    __tablename__ = "course_prerequisites"

    course_id: Mapped[UUID] = mapped_column(ForeignKey("courses.id"), primary_key=True)
    prerequisite_course_id: Mapped[UUID] = mapped_column(ForeignKey("courses.id"), primary_key=True)

    __table_args__ = (
        CheckConstraint("course_id != prerequisite_course_id", name="check_no_self_prerequisite"),
    )
