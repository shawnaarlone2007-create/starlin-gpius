from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Course, Enrollment, User, Role
from .. import db

enrollments_bp = Blueprint("enrollments", __name__)


@enrollments_bp.route("/")
@login_required
def my_enrollments():
    if current_user.role == Role.STUDENT:
        enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    else:
        enrollments = Enrollment.query.all()
    return render_template("enrollments/list.html", enrollments=enrollments)


@enrollments_bp.route("/add", methods=["POST"])
@login_required
def add_enrollment():
    course_id = int(request.form.get("course_id"))
    student_id = int(request.form.get("student_id", current_user.id))

    if current_user.role == Role.STUDENT and student_id != current_user.id:
        flash("You cannot enroll other students.", "danger")
        return redirect(url_for("courses.list_courses"))

    enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if enrollment:
        flash("Student already enrolled.", "info")
        return redirect(url_for("enrollments.my_enrollments"))

    db.session.add(Enrollment(student_id=student_id, course_id=course_id))
    db.session.commit()
    flash("Enrolled successfully.", "success")
    return redirect(url_for("enrollments.my_enrollments"))


@enrollments_bp.route("/remove", methods=["POST"])
@login_required
def remove_enrollment():
    enrollment_id = int(request.form.get("enrollment_id"))
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        flash("Enrollment not found.", "warning")
        return redirect(url_for("enrollments.my_enrollments"))

    if current_user.role == Role.STUDENT and enrollment.student_id != current_user.id:
        flash("You cannot remove enrollments of others.", "danger")
        return redirect(url_for("enrollments.my_enrollments"))

    db.session.delete(enrollment)
    db.session.commit()
    flash("Enrollment removed.", "success")
    return redirect(url_for("enrollments.my_enrollments"))
