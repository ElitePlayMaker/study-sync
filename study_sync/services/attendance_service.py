"""Attendance service — mark and summarize attendance."""

from study_sync.models import attendance as attendance_model
from study_sync.models import booking as booking_model
from study_sync.models import notification as notification_model

VALID_STATUSES = {"present", "absent", "late"}


def mark(booking_id, lecturer_id, status):
    """Mark attendance for a booking."""
    if status not in VALID_STATUSES:
        return False, "Invalid attendance status."

    bookings = booking_model.list_lecturer_bookings(lecturer_id)
    booking = next((b for b in bookings if b["booking_id"] == booking_id), None)
    if not booking:
        return False, "You cannot mark attendance for this booking."

    attendance_model.upsert(booking_id, lecturer_id, status)
    notification_model.create(
        booking["student_id"],
        "Attendance updated",
        f"Attendance marked as {status} for {booking['class_title']}.",
    )
    return True, "Attendance recorded."
