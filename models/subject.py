from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.teacher import Teacher
    from models.grade import Grade


class Subject(Base):
    __tablename__ = 'subjects'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id'), nullable=False)
    teacher: Mapped['Teacher'] = relationship(back_populates='subjects')
    grades: Mapped[List['Grade']] = relationship(back_populates='subject')
    