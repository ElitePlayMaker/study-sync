"""Notification model — in-app alerts for users."""

from study_sync.extensions import get_db


def create(user_id, title, message):
    """Create a notification for a user."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO notifications (user_id, title, message) VALUES (%s, %s, %s)",
            (user_id, title, message),
        )
        db.commit()
        return cursor.lastrowid
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()


def list_for_user(user_id, limit=10):
    """Return recent notifications for a user."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT * FROM notifications
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (user_id, limit),
        )
        return cursor.fetchall()
    finally:
        cursor.close()


def unread_count(user_id):
    """Count unread notifications."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT COUNT(*) FROM notifications WHERE user_id = %s AND is_read = 0",
            (user_id,),
        )
        return cursor.fetchone()[0]
    finally:
        cursor.close()


def mark_read(notification_id, user_id):
    """Mark a single notification as read."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE notifications SET is_read = 1 WHERE id = %s AND user_id = %s",
            (notification_id, user_id),
        )
        db.commit()
        return cursor.rowcount > 0
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()


def mark_all_read(user_id):
    """Mark all notifications as read for a user."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE notifications SET is_read = 1 WHERE user_id = %s AND is_read = 0",
            (user_id,),
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()
