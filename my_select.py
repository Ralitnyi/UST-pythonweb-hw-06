from __future__ import annotations

from typing import List, Dict, Optional

from sqlalchemy import select, func, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from db_source import get_engine
from models.student import Student
from models.group import Group
from models.teacher import Teacher
from models.subject import Subject
from models.grade import Grade


def select_1(session: Session, limit: int = 5) -> List[Dict]:
	"""Find top `limit` students by average grade across all subjects."""
	stmt = (
		select(Student.id, Student.name, func.avg(Grade.value).label("avg"))
		.join(Grade, Grade.student_id == Student.id)
		.group_by(Student.id)
		.order_by(desc(func.avg(Grade.value)))
		.limit(limit)
	)
	rows = session.execute(stmt).all()
	return [{"student_id": r.id, "name": r.name, "avg": float(r.avg)} for r in rows]


def select_2(session: Session, subject_id: int) -> Optional[Dict]:
	"""Find the student with the highest average grade for a given subject."""
	stmt = (
		select(Student.id, Student.name, func.avg(Grade.value).label("avg"))
		.join(Grade, Grade.student_id == Student.id)
		.where(Grade.subject_id == subject_id)
		.group_by(Student.id)
		.order_by(desc(func.avg(Grade.value)))
		.limit(1)
	)
	row = session.execute(stmt).first()
	if not row:
		return None
	return {"student_id": row.id, "name": row.name, "avg": float(row.avg)}


def select_3(session: Session, subject_id: int) -> List[Dict]:
	"""Find average grade per group for a given subject."""
	stmt = (
		select(Group.id, Group.name, func.avg(Grade.value).label("avg"))
		.join(Student, Student.group_id == Group.id)
		.join(Grade, Grade.student_id == Student.id)
		.where(Grade.subject_id == subject_id)
		.group_by(Group.id)
		.order_by(Group.name)
	)
	rows = session.execute(stmt).all()
	return [{"group_id": r.id, "group_name": r.name, "avg": float(r.avg)} for r in rows]


def select_4(session: Session) -> Optional[float]:
	"""Find average grade across all grades (the whole stream)."""
	stmt = select(func.avg(Grade.value).label("avg"))
	row = session.execute(stmt).scalar_one_or_none()
	return float(row) if row is not None else None


def select_5(session: Session, teacher_id: int) -> List[Dict]:
	"""Find subjects taught by a particular teacher."""
	stmt = select(Subject.id, Subject.name).where(Subject.teacher_id == teacher_id)
	rows = session.execute(stmt).all()
	return [{"subject_id": r.id, "name": r.name} for r in rows]


def select_6(session: Session, group_id: int) -> List[Dict]:
	"""List students in a particular group."""
	stmt = select(Student.id, Student.name).where(Student.group_id == group_id).order_by(Student.name)
	rows = session.execute(stmt).all()
	return [{"student_id": r.id, "name": r.name} for r in rows]


def select_7(session: Session, group_id: int, subject_id: int) -> List[Dict]:
	"""Find grades of students in a specific group for a specific subject."""
	stmt = (
		select(Student.id.label("student_id"), Student.name.label("student_name"), Grade.value, Grade.date_received)
		.join(Grade, Grade.student_id == Student.id)
		.where(Student.group_id == group_id, Grade.subject_id == subject_id)
		.order_by(Student.name, Grade.date_received)
	)
	rows = session.execute(stmt).all()
	return [
		{
			"student_id": r.student_id,
			"student_name": r.student_name,
			"value": int(r.value),
			"date_received": r.date_received.isoformat() if r.date_received else None,
		}
		for r in rows
	]


def select_8(session: Session, teacher_id: int) -> Optional[float]:
	"""Find average grade given by a particular teacher across the subjects they teach."""
	stmt = (
		select(func.avg(Grade.value).label("avg"))
		.join(Subject, Subject.id == Grade.subject_id)
		.where(Subject.teacher_id == teacher_id)
	)
	row = session.execute(stmt).scalar_one_or_none()
	return float(row) if row is not None else None


def select_9(session: Session, student_id: int) -> List[Dict]:
	"""List distinct subjects a student attends (has grades for)."""
	stmt = (
		select(Subject.id, Subject.name)
		.join(Grade, Grade.subject_id == Subject.id)
		.where(Grade.student_id == student_id)
		.distinct()
	)
	rows = session.execute(stmt).all()
	return [{"subject_id": r.id, "name": r.name} for r in rows]


def select_10(session: Session, student_id: int, teacher_id: int) -> List[Dict]:
	"""List subjects that a given teacher teaches to a given student."""
	stmt = (
		select(Subject.id, Subject.name)
		.join(Grade, Grade.subject_id == Subject.id)
		.where(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
		.distinct()
	)
	rows = session.execute(stmt).all()
	return [{"subject_id": r.id, "name": r.name} for r in rows]

if __name__ == "__main__":
    engine = get_engine()
    Session = sessionmaker(engine, future=True)
    with Session() as session:
        top5 = select_1(session, limit=5)
        print("=== select_1: top students by average grade ===")
        print(select_1(session, limit=5))
        print("\n=== select_2: top student for subject 1 ===")
        print(select_2(session, subject_id=1))
        print("\n=== select_3: average grade per group for subject 1 ===")
        print(select_3(session, subject_id=1))
        print("\n=== select_4: average grade across all grades ===")
        print(select_4(session))
        print("\n=== select_5: subjects taught by teacher 1 ===")
        print(select_5(session, teacher_id=1))
        print("\n=== select_6: students in group 1 ===")
        print(select_6(session, group_id=1))
        print("\n=== select_7: grades for group 1 and subject 1 ===")
        print(select_7(session, group_id=1, subject_id=1))
        print("\n=== select_8: average grade for teacher 1 ===")
        print(select_8(session, teacher_id=1))
        print("\n=== select_9: subjects student 1 attends ===")
        print(select_9(session, student_id=1))
        print("\n=== select_10: subjects teacher 1 teaches to student 1 ===")
        print(select_10(session, student_id=1, teacher_id=1))