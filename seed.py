from __future__ import annotations

import argparse
import random
from typing import Dict, List

from faker import Faker
from sqlalchemy.orm import Session, sessionmaker

from models.base import Base
from models.group import Group
from models.student import Student
from models.teacher import Teacher
from models.subject import Subject
from models.grade import Grade

from db_source import get_engine

def create_tables(engine) -> None:
    Base.metadata.create_all(engine)


def create_groups(session: Session, n: int) -> List[Group]:
    groups = [Group(name=f"Group {i+1}") for i in range(n)]
    session.add_all(groups)
    session.flush()
    return groups


def create_teachers(session: Session, n: int, fake: Faker) -> List[Teacher]:
    teachers = [Teacher(name=fake.name()) for _ in range(n)]
    session.add_all(teachers)
    session.flush()
    return teachers


def create_subjects(session: Session, n: int, teachers: List[Teacher], fake: Faker) -> List[Subject]:
    subjects: List[Subject] = []
    for _ in range(n):
        subj = Subject(name=fake.word().title(), teacher=random.choice(teachers))
        subjects.append(subj)
    session.add_all(subjects)
    session.flush()
    return subjects


def create_students(session: Session, n: int, groups: List[Group], fake: Faker) -> List[Student]:
    students = [Student(name=fake.name(), group=random.choice(groups)) for _ in range(n)]
    session.add_all(students)
    session.flush()
    return students


def create_grades(session: Session, students: List[Student], subjects: List[Subject], max_per_student: int, fake: Faker) -> List[Grade]:
    grades: List[Grade] = []
    for student in students:
        n = random.randint(5, max_per_student)
        for _ in range(n):
            g = Grade(
                student=student,
                subject=random.choice(subjects),
                value=random.randint(1, 12),
                date_received=fake.date_between(start_date='-1y', end_date='today'),
            )
            grades.append(g)
    session.add_all(grades)
    session.flush()
    return grades


def seed(
    *,
    groups_n: int = 3,
    teachers_n: int = 4,
    subjects_n: int = 6,
    students_n: int = 40,
    max_grades_per_student: int = 20,
    echo: bool = False,
) -> Dict[str, int]:
    fake = Faker()
    engine = get_engine(echo=echo)
    SessionLocal = sessionmaker(engine, future=True)

    create_tables(engine)

    with SessionLocal() as session:
        groups = create_groups(session, groups_n)
        teachers = create_teachers(session, teachers_n, fake)
        subjects = create_subjects(session, subjects_n, teachers, fake)
        students = create_students(session, students_n, groups, fake)
        grades = create_grades(session, students, subjects, max_grades_per_student, fake)

        session.commit()

    return {
        "groups": len(groups),
        "teachers": len(teachers),
        "subjects": len(subjects),
        "students": len(students),
        "grades": len(grades),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed the database with fake data")
    parser.add_argument("--groups", type=int, default=3)
    parser.add_argument("--teachers", type=int, default=4)
    parser.add_argument("--subjects", type=int, default=6)
    parser.add_argument("--students", type=int, default=40)
    parser.add_argument("--max-grades", type=int, default=20)
    parser.add_argument("--echo", action="store_true", help="Show SQL statements")

    args = parser.parse_args()

    print("Seeding database...")
    result = seed(
        groups_n=args.groups,
        teachers_n=args.teachers,
        subjects_n=args.subjects,
        students_n=args.students,
        max_grades_per_student=args.max_grades,
        echo=args.echo,
    )
    print("Done. Summary:")
    for k, v in result.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
