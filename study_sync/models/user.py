"""User model — database access for accounts and profiles."""

from study_sync.extensions import get_db


def find_by_email(email, role=None):
    """Fetch a user by email, optionally filtered by role."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        if role:
            cursor.execute(
                "SELECT * FROM users WHERE email = %s AND role = %s",
                (email.lower(), role),
            )
        else:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email.lower(),))
        return cursor.fetchone()
    finally:
        cursor.close()


def find_by_id(user_id):
    """Fetch a single user by primary key."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close()


def create_user(name, email, password_hash, role="student", phone=None, department=None):
    """Insert a new user record."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (name, email, password_hash, role, phone, department)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (name, email.lower(), password_hash, role, phone, department),
        )
        db.commit()
        return cursor.lastrowid
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()


def update_profile(user_id, name, phone, bio, department):
    """Update editable profile fields."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            UPDATE users
            SET name = %s, phone = %s, bio = %s, department = %s
            WHERE id = %s
            """,
            (name, phone, bio, department, user_id),
        )
        db.commit()
        return cursor.rowcount > 0
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()


def count_by_role(role):
    """Count users for admin dashboard metrics."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = %s", (role,))
        return cursor.fetchone()[0]
    finally:
        cursor.close()
