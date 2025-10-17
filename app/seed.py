from . import db
from .models import User, Role, Course, Enrollment

def seed_data():
    db.create_all()

    # Admin
    admin_email = "admin@example.com"
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(email=admin_email, name="Admin", role=Role.ADMIN)
        admin.set_password("admin123")
        db.session.add(admin)

    # Teacher
    teacher_email = "teacher@example.com"
    teacher = User.query.filter_by(email=teacher_email).first()
    if not teacher:
        teacher = User(email=teacher_email, name="Teacher Tom", role=Role.TEACHER)
        teacher.set_password("teacher123")
        db.session.add(teacher)

    # Student
    student_email = "student@example.com"
    student = User.query.filter_by(email=student_email).first()
    if not student:
        student = User(email=student_email, name="Student Sue", role=Role.STUDENT)
        student.set_password("student123")
        db.session.add(student)

    db.session.commit()

    # Course
    sample_course = Course.query.filter_by(title="Math 101").first()
    if not sample_course:
        sample_course = Course(title="Math 101", description="Basics of Algebra", teacher_id=teacher.id)
        db.session.add(sample_course)
        db.session.commit()

    # Enrollment
    enrollment = Enrollment.query.filter_by(student_id=student.id, course_id=sample_course.id).first()
    if not enrollment:
        db.session.add(Enrollment(student_id=student.id, course_id=sample_course.id))
        db.session.commit()
