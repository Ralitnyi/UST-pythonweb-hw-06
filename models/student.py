from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.group import Group
    from models.grade import Grade


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'), nullable=False)
    group: Mapped['Group'] = relationship(back_populates='students')
    grades: Mapped[list['Grade']] = relationship(back_populates='student')
    