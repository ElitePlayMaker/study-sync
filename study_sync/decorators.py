"""Route decorators for authentication and role-based access."""

from functools import wraps

from flask import flash, redirect, session, url_for


def login_required(*roles):
    """Require an authenticated session and optionally specific role(s)."""

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                flash("Please sign in to continue.", "warning")
                return redirect(url_for("auth.student_login"))

            if roles and session.get("role") not in roles:
                flash("You do not have permission to access that page.", "danger")
                return redirect(url_for("public.landing"))

            return view(*args, **kwargs)

        return wrapped

    return decorator
