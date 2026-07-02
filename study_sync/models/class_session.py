"""Class and time-slot model — database access for sessions."""

from study_sync.extensions import get_db


def list_classes(search=None, category=None, lecturer_id=None):
    """Return classes with optional search and filter parameters."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        query = """
            SELECT c.*, u.name AS lecturer_name,
                   (SELECT COUNT(*) FROM time_slots ts WHERE ts.class_id = c.id) AS slot_count
            FROM classes c
            JOIN users u ON u.id = c.lecturer_id
            WHERE c.status = 'active'
        """
        params = []

        if lecturer_id:
            query += " AND c.lecturer_id = %s"
            params.append(lecturer_id)

        if category:
            query += " AND c.category = %s"
            params.append(category)

        if search:
            query += " AND (c.title LIKE %s OR c.description LIKE %s OR u.name LIKE %s)"
            like = f"%{search}%"
            params.extend([like, like, like])

        query += " ORDER BY c.title ASC"
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    finally:
        cursor.close()


def get_class(class_id):
    """Fetch one class with lecturer details."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT c.*, u.name AS lecturer_name, u.email AS lecturer_email
            FROM classes c
            JOIN users u ON u.id = c.lecturer_id
            WHERE c.id = %s
            """,
            (class_id,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()


def create_class(title, description, lecturer_id, category, location, duration_minutes):
    """Create a new class offering."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO classes (title, description, lecturer_id, category, location, duration_minutes)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (title, description, lecturer_id, category, location, duration_minutes),
        )
        db.commit()
        return cursor.lastrowid
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()


def update_class(class_id, title, description, category, location, duration_minutes, status):
    """Update class metadata."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            UPDATE classes
            SET title = %s, description = %s, category = %s,
                location = %s, duration_minutes = %s, status = %s
            WHERE id = %s
            """,
            (title, description, category, location, duration_minutes, status, class_id),
        )
        db.commit()
        return cursor.rowcount > 0
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()


def delete_class(class_id):
    """Remove a class and cascade related slots/bookings."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM classes WHERE id = %s", (class_id,))
        db.commit()
        return cursor.rowcount > 0
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()


def list_slots_for_class(class_id, only_open=False):
    """List time slots for a class."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        query = """
            SELECT ts.*,
                   (SELECT COUNT(*) FROM bookings b
                    WHERE b.slot_id = ts.id AND b.status = 'confirmed') AS booked_count
            FROM time_slots ts
            WHERE ts.class_id = %s
        """
        params = [class_id]
        if only_open:
            query += " AND ts.status = 'open'"
        query += " ORDER BY ts.start_time ASC"
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    finally:
        cursor.close()


def get_slot(slot_id, for_update=False):
    """Fetch a single time slot, optionally with row lock."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        lock = " FOR UPDATE" if for_update else ""
        cursor.execute(f"SELECT * FROM time_slots WHERE id = %s{lock}", (slot_id,))
        return cursor.fetchone()
    finally:
        cursor.close()


def create_slot(class_id, start_time, end_time, max_capacity):
    """Add a bookable time slot to a class."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO time_slots (class_id, start_time, end_time, max_capacity)
            VALUES (%s, %s, %s, %s)
            """,
            (class_id, start_time, end_time, max_capacity),
        )
        db.commit()
        return cursor.lastrowid
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()


def calendar_events(start_date=None, end_date=None, lecturer_id=None):
    """Return slot events for calendar views."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        query = """
            SELECT ts.id AS slot_id, ts.start_time, ts.end_time, ts.max_capacity, ts.status,
                   c.id AS class_id, c.title, c.category, c.location,
                   u.name AS lecturer_name,
                   (SELECT COUNT(*) FROM bookings b
                    WHERE b.slot_id = ts.id AND b.status = 'confirmed') AS booked_count
            FROM time_slots ts
            JOIN classes c ON c.id = ts.class_id
            JOIN users u ON u.id = c.lecturer_id
            WHERE c.status = 'active'
        """
        params = []
        if lecturer_id:
            query += " AND c.lecturer_id = %s"
            params.append(lecturer_id)
        if start_date:
            query += " AND ts.start_time >= %s"
            params.append(start_date)
        if end_date:
            query += " AND ts.start_time <= %s"
            params.append(end_date)
        query += " ORDER BY ts.start_time ASC"
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    finally:
        cursor.close()


def distinct_categories():
    """Return unique class categories for filter dropdowns."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT DISTINCT category FROM classes WHERE status = 'active' ORDER BY category"
        )
        return [row[0] for row in cursor.fetchall()]
    finally:
        cursor.close()
