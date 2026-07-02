"""Booking service — time-slot reservations with double-booking prevention."""

from datetime import datetime

import mysql.connector

from study_sync.models import booking as booking_model
from study_sync.models import class_session as class_model
from study_sync.models import notification as notification_model
from study_sync.utils.email import send_booking_confirmation


def book_slot(student_id, slot_id):
    """
    Book a time slot for a student.
    Prevents double booking via app checks and DB unique constraint.
    """
    slot = class_model.get_slot(slot_id, for_update=True)
    if not slot:
        return False, "Time slot not found."

    if slot["status"] != "open":
        return False, "This time slot is not available."

    if booking_model.student_has_booking(student_id, slot_id):
        return False, "You have already booked this slot."

    booked = booking_model.count_confirmed_for_slot(slot_id)
    if booked >= slot["max_capacity"]:
        return False, "This time slot is fully booked."

    try:
        booking_id = booking_model.create_booking(student_id, slot_id)
    except mysql.connector.Error as err:
        if err.errno == 1062:
            return False, "You have already booked this slot."
        raise

    details = booking_model.get_booking_details(booking_id)
    slot_time = details["start_time"].strftime("%Y-%m-%d %H:%M")
    send_booking_confirmation(
        details["student_email"],
        details["student_name"],
        details["class_title"],
        slot_time,
    )
    notification_model.create(
        student_id,
        "Booking confirmed",
        f"You are booked for {details['class_title']} on {slot_time}.",
    )
    return True, "Booking confirmed. Check your email for details."


def cancel(student_id, booking_id):
    """Cancel a student booking."""
    if booking_model.cancel_booking(booking_id, student_id):
        notification_model.create(
            student_id,
            "Booking cancelled",
            "Your session booking was cancelled successfully.",
        )
        return True, "Booking cancelled."
    return False, "Booking not found or already cancelled."
