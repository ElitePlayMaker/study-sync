"""Email notification placeholders for booking confirmations."""

import logging

from flask import current_app

logger = logging.getLogger(__name__)


def send_booking_confirmation(student_email, student_name, class_title, slot_time):
    """Placeholder for booking confirmation emails."""
    subject = f"Booking Confirmed — {class_title}"
    body = (
        f"Hi {student_name},\n\n"
        f"Your Study Sync session is confirmed.\n\n"
        f"Class: {class_title}\n"
        f"Time: {slot_time}\n\n"
        f"See you there!\n"
        f"— {current_app.config['APP_NAME']} Team"
    )

    if current_app.config.get("MAIL_ENABLED"):
        logger.info("EMAIL [%s] -> %s", subject, student_email)
    else:
        logger.info("EMAIL PLACEHOLDER | to=%s | subject=%s", student_email, subject)

    return True


def send_contact_acknowledgement(name, email):
    """Placeholder acknowledgement for contact form submissions."""
    logger.info("CONTACT ACK PLACEHOLDER | name=%s | email=%s", name, email)
    return True
