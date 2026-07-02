"""Lecturer routes — class management, attendance, profile."""

from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from study_sync.decorators import login_required
from study_sync.models import attendance as attendance_model
from study_sync.models import booking as booking_model
from study_sync.models import class_session as class_model
from study_sync.models import notification as notification_model
from study_sync.models import user as user_model
from study_sync.services import attendance_service, auth_service, class_service

lecturer_bp = Blueprint("lecturer", __name__, url_prefix="/lecturer")


@lecturer_bp.route("/dashboard")
@login_required("lecturer")
def dashboard():
    """Lecturer overview with classes and upcoming bookings."""
    lecturer_id = session["user_id"]
    classes = class_model.list_classes(lecturer_id=lecturer_id)
    bookings = booking_model.list_lecturer_bookings(lecturer_id)
    attendance_stats = attendance_model.stats_for_lecturer(lecturer_id)
    notifications = notification_model.list_for_user(lecturer_id, limit=6)
    return render_template(
        "lecturer/dashboard.html",
        classes=classes,
        bookings=bookings[:10],
        attendance_stats=attendance_stats,
        notifications=notifications,
    )


@lecturer_bp.route("/classes/create", methods=["POST"])
@login_required("lecturer")
def create_class():
    """Create class with initial time slot."""
    try:
        start = datetime.strptime(request.form.get("start_time", ""), "%Y-%m-%dT%H:%M")
        end = datetime.strptime(request.form.get("end_time", ""), "%Y-%m-%dT%H:%M")
    except ValueError:
        flash("Invalid date/time format.", "danger")
        return redirect(url_for("lecturer.dashboard"))

    ok, result = class_service.create_class_with_slot(
        title=request.form.get("title", "").strip(),
        description=request.form.get("description", "").strip(),
        lecturer_id=session["user_id"],
        category=request.form.get("category", "General").strip(),
        location=request.form.get("location", "Online").strip(),
        duration_minutes=int(request.form.get("duration_minutes", 60)),
        start_time=start,
        end_time=end,
        max_capacity=int(request.form.get("max_capacity", 10)),
    )
    flash("Class created successfully." if ok else result, "success" if ok else "danger")
    return redirect(url_for("lecturer.dashboard"))


@lecturer_bp.route("/classes/<int:class_id>/slots", methods=["POST"])
@login_required("lecturer")
def add_slot(class_id):
    """Add another time slot to a class."""
    try:
        start = datetime.strptime(request.form.get("start_time", ""), "%Y-%m-%dT%H:%M")
        end = datetime.strptime(request.form.get("end_time", ""), "%Y-%m-%dT%H:%M")
    except ValueError:
        flash("Invalid date/time format.", "danger")
        return redirect(url_for("lecturer.dashboard"))

    ok, message = class_service.add_slot(
        class_id, start, end,
        int(request.form.get("max_capacity", 10)),
        lecturer_id=session["user_id"],
    )
    flash(message, "success" if ok else "danger")
    return redirect(url_for("lecturer.dashboard"))


@lecturer_bp.route("/attendance/<int:booking_id>", methods=["POST"])
@login_required("lecturer")
def mark_attendance(booking_id):
    """Mark attendance for a student booking."""
    status = request.form.get("status", "present")
    ok, message = attendance_service.mark(booking_id, session["user_id"], status)
    flash(message, "success" if ok else "danger")
    return redirect(url_for("lecturer.dashboard"))


@lecturer_bp.route("/calendar")
@login_required("lecturer")
def calendar():
    """Lecturer calendar view."""
    return render_template("lecturer/calendar.html")


@lecturer_bp.route("/api/calendar-events")
@login_required("lecturer")
def calendar_events():
    """JSON calendar events for lecturer."""
    events = class_service.calendar_data(lecturer_id=session["user_id"])
    return jsonify(events)


@lecturer_bp.route("/profile", methods=["GET", "POST"])
@login_required("lecturer")
def profile():
    """Lecturer profile."""
    user = user_model.find_by_id(session["user_id"])
    if request.method == "POST":
        ok, message = auth_service.update_profile(
            session["user_id"],
            request.form.get("name", ""),
            request.form.get("phone", ""),
            request.form.get("bio", ""),
            request.form.get("department", ""),
        )
        flash(message, "success" if ok else "danger")
        session["name"] = request.form.get("name", session["name"])
        return redirect(url_for("lecturer.profile"))
    return render_template("lecturer/profile.html", user=user)
