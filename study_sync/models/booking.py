"""Booking model — database access for student reservations."""

from study_sync.extensions import get_db


def create_booking(student_id, slot_id):
    """Insert a confirmed booking."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO bookings (student_id, slot_id, status)
            VALUES (%s, %s, 'confirmed')
            """,
            (student_id, slot_id),
        )
        db.commit()
        return cursor.lastrowid
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()


def cancel_booking(booking_id, student_id):
    """Cancel a booking owned by the given student."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            UPDATE bookings
            SET status = 'cancelled'
            WHERE id = %s AND student_id = %s AND status = 'confirmed'
            """,
            (booking_id, student_id),
        )
        db.commit()
        return cursor.rowcount > 0
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()


def count_confirmed_for_slot(slot_id):
    """Count active bookings on a slot."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT COUNT(*) FROM bookings WHERE slot_id = %s AND status = 'confirmed'",
            (slot_id,),
        )
        return cursor.fetchone()[0]
    finally:
        cursor.close()


def student_has_booking(student_id, slot_id):
    """Check if student already booked this slot."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            SELECT id FROM bookings
            WHERE student_id = %s AND slot_id = %s AND status = 'confirmed'
            """,
            (student_id, slot_id),
        )
        return cursor.fetchone() is not None
    finally:
        cursor.close()


def list_student_bookings(student_id):
    """Return all bookings for a student with class/slot details."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT b.id AS booking_id, b.slot_id, b.status, b.booked_at, ts.start_time, ts.end_time,
                   c.id AS class_id, c.title, c.category, c.location,
                   u.name AS lecturer_name,
                   a.status AS attendance_status
            FROM bookings b
            JOIN time_slots ts ON ts.id = b.slot_id
            JOIN classes c ON c.id = ts.class_id
            JOIN users u ON u.id = c.lecturer_id
            LEFT JOIN attendance a ON a.booking_id = b.id
            WHERE b.student_id = %s
            ORDER BY ts.start_time DESC
            """,
            (student_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()


def list_lecturer_bookings(lecturer_id):
    """Return bookings for all classes owned by a lecturer."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT b.id AS booking_id, b.student_id, b.status, b.booked_at, s.name AS student_name, s.email AS student_email,
                   ts.start_time, ts.end_time,
                   c.title AS class_title,
                   a.status AS attendance_status, a.id AS attendance_id
            FROM bookings b
            JOIN users s ON s.id = b.student_id
            JOIN time_slots ts ON ts.id = b.slot_id
            JOIN classes c ON c.id = ts.class_id
            LEFT JOIN attendance a ON a.booking_id = b.id
            WHERE c.lecturer_id = %s AND b.status = 'confirmed'
            ORDER BY ts.start_time ASC
            """,
            (lecturer_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()


def get_booking_details(booking_id):
    """Fetch booking with student and class info for emails."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT b.*, s.name AS student_name, s.email AS student_email,
                   c.title AS class_title, ts.start_time, ts.end_time
            FROM bookings b
            JOIN users s ON s.id = b.student_id
            JOIN time_slots ts ON ts.id = b.slot_id
            JOIN classes c ON c.id = ts.class_id
            WHERE b.id = %s
            """,
            (booking_id,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()


def count_all_confirmed():
    """Total confirmed bookings for admin metrics."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM bookings WHERE status = 'confirmed'")
        return cursor.fetchone()[0]
    finally:
        cursor.close()


