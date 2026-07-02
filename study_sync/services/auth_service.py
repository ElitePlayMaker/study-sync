"""Authentication service — registration, login, session helpers."""

from werkzeug.security import check_password_hash, generate_password_hash

from study_sync.models import notification as notification_model
from study_sync.models import user as user_model


def register_student(name, email, password, phone=None, department=None):
    """Register a new student account."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    if user_model.find_by_email(email):
        return False, "An account with this email already exists."

    password_hash = generate_password_hash(password)
    user_id = user_model.create_user(
        name=name,
        email=email,
        password_hash=password_hash,
        role="student",
        phone=phone,
        department=department,
    )
    notification_model.create(
        user_id,
        "Welcome to Study Sync",
        "Your account is ready. Browse classes and book your first session.",
    )
    return True, user_id


def authenticate(email, password, role):
    """Validate credentials for a specific role."""
    user = user_model.find_by_email(email, role=role)
    if not user or not check_password_hash(user["password_hash"], password):
        return None
    return user


def build_session(user):
    """Return session payload for Flask session storage."""
    return {
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
    }


def update_profile(user_id, name, phone, bio, department):
    """Update user profile fields."""
    if not name.strip():
        return False, "Name is required."
    user_model.update_profile(user_id, name.strip(), phone, bio, department)
    return True, "Profile updated successfully."
