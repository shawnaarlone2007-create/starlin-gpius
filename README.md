# School Portal (Flask)

A simple school portal with authentication, role-based dashboards, courses, and enrollments.

## Features
- Authentication (login/logout)
- Roles: admin, teacher, student
- Courses list and creation (admin/teacher)
- Enrollments list; students can enroll self; admins/teachers manage

## Setup
1. Create and activate a virtualenv (Python 3.10+):
```bash
python3 -m venv .venv
source .venv/bin/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Configure environment (optional):
```bash
cp .env.example .env
```
4. Initialize and seed the database:
```bash
python -m flask --app wsgi db upgrade || python -m flask --app wsgi init-db
python -m flask --app wsgi seed
```
5. Run the app:
```bash
python wsgi.py
```

## Default accounts
- admin@example.com / admin123
- teacher@example.com / teacher123
- student@example.com / student123
