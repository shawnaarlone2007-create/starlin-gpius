from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def dashboard():
    return render_template("dashboard/index.html", user=current_user)
