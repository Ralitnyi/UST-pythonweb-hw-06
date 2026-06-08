from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.student import Student
    from models.subject import Subject


class Grade(Base):
    __tablename__ = 'grades'

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id'), nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    date_received: Mapped[date] = mapped_column(Date, nullable=False)

    student: Mapped['Student'] = relationship(back_populates='grades')
    subject: Mapped['Subject'] = relationship(back_populates='grades')
