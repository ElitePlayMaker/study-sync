"""Student routes — dashboard, booking, calendar, profile."""

from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from study_sync.decorators import login_required
from study_sync.models import booking as booking_model
from study_sync.models import class_session as class_model
from study_sync.models import notification as notification_model
from study_sync.models import user as user_model
from study_sync.services import auth_service, booking_service, class_service

student_bp = Blueprint("student", __name__, url_prefix="/student")


@student_bp.route("/dashboard")
@login_required("student")
def dashboard():
    """Student home dashboard with bookings and notifications."""
    user_id = session["user_id"]
    bookings = booking_model.list_student_bookings(user_id)
    upcoming = [b for b in bookings if b["status"] == "confirmed"][:5]
    notifications = notification_model.list_for_user(user_id, limit=8)
    unread = notification_model.unread_count(user_id)
    return render_template(
        "student/dashboard.html",
        upcoming=upcoming,
        bookings=bookings,
        notifications=notifications,
        unread=unread,
    )


@student_bp.route("/classes")
@login_required("student")
def browse_classes():
    """Searchable class catalog."""
    search = request.args.get("q", "").strip() or None
    category = request.args.get("category", "").strip() or None
    classes = class_service.search_classes(search=search, category=category)
    categories = class_model.distinct_categories()
    return render_template(
        "student/booking.html",
        classes=classes,
        categories=categories,
        search=search or "",
        selected_category=category or "",
    )


@student_bp.route("/classes/<int:class_id>")
@login_required("student")
def class_detail(class_id):
    """Class detail with available time slots."""
    class_item = class_model.get_class(class_id)
    if not class_item:
        flash("Class not found.", "danger")
        return redirect(url_for("student.browse_classes"))

    slots = class_model.list_slots_for_class(class_id, only_open=True)
    student_bookings = booking_model.list_student_bookings(session["user_id"])
    booked_slot_ids = {
        b["slot_id"] for b in student_bookings
        if b["status"] == "confirmed" and b.get("class_id") == class_id
    }
    return render_template(
        "student/class_detail.html",
        class_item=class_item,
        slots=slots,
        booked_slot_ids=booked_slot_ids,
    )


@student_bp.route("/book/<int:slot_id>", methods=["POST"])
@login_required("student")
def book_slot(slot_id):
    """Book a specific time slot."""
    ok, message = booking_service.book_slot(session["user_id"], slot_id)
    flash(message, "success" if ok else "warning")
    slot = class_model.get_slot(slot_id)
    if slot:
        return redirect(url_for("student.class_detail", class_id=slot["class_id"]))
    return redirect(url_for("student.browse_classes"))


@student_bp.route("/cancel/<int:booking_id>", methods=["POST"])
@login_required("student")
def cancel_booking(booking_id):
    """Cancel a booking."""
    ok, message = booking_service.cancel(session["user_id"], booking_id)
    flash(message, "success" if ok else "warning")
    return redirect(url_for("student.dashboard"))


@student_bp.route("/calendar")
@login_required("student")
def calendar():
    """Calendar view of available sessions."""
    return render_template("student/calendar.html")


@student_bp.route("/api/calendar-events")
@login_required("student")
def calendar_events():
    """JSON feed for FullCalendar."""
    events = class_service.calendar_data()
    return jsonify(events)


@student_bp.route("/profile", methods=["GET", "POST"])
@login_required("student")
def profile():
    """Student profile page."""
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
        return redirect(url_for("student.profile"))

    return render_template("student/profile.html", user=user)


@student_bp.route("/notifications/read/<int:notification_id>", methods=["POST"])
@login_required("student")
def mark_notification(notification_id):
    """Mark one notification as read."""
    notification_model.mark_read(notification_id, session["user_id"])
    return redirect(request.referrer or url_for("student.dashboard"))


@student_bp.route("/notifications/read-all", methods=["POST"])
@login_required("student")
def mark_all_notifications():
    """Mark all notifications as read."""
    notification_model.mark_all_read(session["user_id"])
    flash("All notifications marked as read.", "info")
    return redirect(url_for("student.dashboard"))


