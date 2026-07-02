"""Attendance model — track session participation."""

from study_sync.extensions import get_db


def upsert(booking_id, marked_by, status):
    """Create or update attendance for a booking."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM attendance WHERE booking_id = %s", (booking_id,))
        existing = cursor.fetchone()
        if existing:
            cursor.execute(
                """
                UPDATE attendance
                SET status = %s, marked_by = %s, marked_at = CURRENT_TIMESTAMP
                WHERE booking_id = %s
                """,
                (status, marked_by, booking_id),
            )
        else:
            cursor.execute(
                """
                INSERT INTO attendance (booking_id, marked_by, status)
                VALUES (%s, %s, %s)
                """,
                (booking_id, marked_by, status),
            )
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()


def stats_for_lecturer(lecturer_id):
    """Attendance summary for lecturer dashboard."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT a.status, COUNT(*) AS total
            FROM attendance a
            JOIN bookings b ON b.id = a.booking_id
            JOIN time_slots ts ON ts.id = b.slot_id
            JOIN classes c ON c.id = ts.class_id
            WHERE c.lecturer_id = %s
            GROUP BY a.status
            """,
            (lecturer_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
