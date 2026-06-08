# 📚 Student Management System

A comprehensive system for managing students, teachers, and grades in an educational institution built with SQLAlchemy and PostgreSQL.

## 🎯 Project Overview

This project demonstrates work with:
- **SQLAlchemy ORM** – object-relational mapping for database operations
- **Alembic** – database migration management
- **PostgreSQL** – relational database
- **Docker** – containerization

### Core Entities

- **Students** – student data and group assignments
- **Teachers** – teacher information and their subjects
- **Groups** – student groups
- **Subjects** – academic disciplines taught by teachers
- **Grades** – student grades for subjects

## 🚀 Quick Start

### Requirements
- Python ≥ 3.12
- Docker and Docker Compose
- PostgreSQL (in container)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd app
```

2. Create virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

3. Start PostgreSQL with Docker Compose:
```bash
docker-compose up -d
```

4. Create tables and populate with sample data:
```bash
python seed.py
```

## 📁 Project Structure

```
├── models/              # SQLAlchemy models
│   ├── base.py         # Base class for models
│   ├── student.py      # Student model
│   ├── teacher.py      # Teacher model
│   ├── group.py        # Group model
│   ├── subject.py      # Subject model
│   └── grade.py        # Grade model
├── alembic/            # Database migrations
│   ├── env.py
│   └── versions/       # Migration files
├── database.py         # Database configuration
├── db_source.py        # Database engine source
├── main.py             # Database connection check
├── seed.py             # Populate database with sample data
├── my_select.py        # Analytical queries
├── docker-compose.yml  # Docker composition
├── Dockerfile          # Dockerfile for image build
├── pyproject.toml      # Project dependencies
└── alembic.ini         # Alembic configuration
```

## 🔧 Usage

### Check database connection
```bash
python main.py
```

### Populate database with sample data
```bash
# Basic population
python seed.py

# With custom counts
python seed.py -n 5 -t 3 -s 10 -st 50 -g 5
```

**Parameters:**
- `-n` – number of groups (default: 3)
- `-t` – number of teachers (default: 4)
- `-s` – number of subjects (default: 6)
- `-st` – number of students (default: 50)
- `-g` – max grades per student (default: 20)

### Run analytical queries
```bash
python my_select.py
```

Available queries:
- **select_1()** – Top students by average grade
- **select_2()** – Student with highest average grade for a subject
- **select_3()** – Average grades by groups for a subject
- and more...

## 📦 Dependencies

- **alembic** ≥ 1.18.4 – database migration management
- **faker** ≥ 40.21.0 – test data generation
- **psycopg** ≥ 3.3.4 – PostgreSQL adapter
- **sqlalchemy** ≥ 2.0.50 – ORM framework

## 🐳 Docker

### Run with Docker Compose
```bash
docker-compose up
```

PostgreSQL service will be available at `localhost:5432`.

### Environment Variables
```
DATABASE_URL=postgresql://user:password@localhost:5432/students_db
```

## 🔄 Database Migrations (Alembic)

### Create a new migration
```bash
alembic revision --autogenerate -m "Description of migration"
```

### Apply migrations
```bash
alembic upgrade head
```

### Revert to previous version
```bash
alembic downgrade -1
```

## 📝 License

MIT

## 👨‍💻 Author

[Your Name]
