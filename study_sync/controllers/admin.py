"""Admin routes — platform oversight and user/class management."""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from study_sync.decorators import login_required
from study_sync.models import booking as booking_model
from study_sync.models import class_session as class_model
from study_sync.models import notification as notification_model
from study_sync.models import user as user_model

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@login_required("admin")
def dashboard():
    """Admin analytics and management dashboard."""
    stats = {
        "students": user_model.count_by_role("student"),
        "lecturers": user_model.count_by_role("lecturer"),
        "bookings": booking_model.count_all_confirmed(),
    }
    classes = class_model.list_classes()
    notifications = notification_model.list_for_user(session["user_id"], limit=6)
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        classes=classes,
        notifications=notifications,
    )


@admin_bp.route("/classes/<int:class_id>/delete", methods=["POST"])
@login_required("admin")
def delete_class(class_id):
    """Admin can remove any class."""
    if class_model.delete_class(class_id):
        flash("Class removed.", "success")
    else:
        flash("Class not found.", "warning")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/classes/<int:class_id>/edit", methods=["GET", "POST"])
@login_required("admin")
def edit_class(class_id):
    """Admin edit class metadata."""
    class_item = class_model.get_class(class_id)
    if not class_item:
        flash("Class not found.", "danger")
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        class_model.update_class(
            class_id,
            request.form.get("title", "").strip(),
            request.form.get("description", "").strip(),
            request.form.get("category", "General").strip(),
            request.form.get("location", "Online").strip(),
            int(request.form.get("duration_minutes", 60)),
            request.form.get("status", "active"),
        )
        flash("Class updated.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/edit_class.html", class_item=class_item)
