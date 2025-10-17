from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Course, User, Role
from .. import db

courses_bp = Blueprint("courses", __name__)


def require_teacher_or_admin() -> bool:
    return current_user.is_authenticated and current_user.role in {Role.ADMIN, Role.TEACHER}


@courses_bp.route("/")
@login_required
def list_courses():
    courses = Course.query.all()
    return render_template("courses/list.html", courses=courses)


@courses_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_course():
    if not require_teacher_or_admin():
        flash("You do not have permission to create courses.", "warning")
        return redirect(url_for("courses.list_courses"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        teacher_id = current_user.id if current_user.role == Role.TEACHER else request.form.get("teacher_id")
        if not title:
            flash("Title is required.", "danger")
            return render_template("courses/create.html")
        if not teacher_id:
            flash("Teacher is required.", "danger")
            return render_template("courses/create.html")
        course = Course(title=title, description=description, teacher_id=int(teacher_id))
        db.session.add(course)
        db.session.commit()
        flash("Course created.", "success")
        return redirect(url_for("courses.list_courses"))

    teachers = User.query.filter(User.role.in_([Role.TEACHER, Role.ADMIN])).all()
    return render_template("courses/create.html", teachers=teachers)
