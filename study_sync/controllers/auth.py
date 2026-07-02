"""Authentication routes — registration and role-specific logins."""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from study_sync.services import auth_service

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Student registration."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        phone = request.form.get("phone", "").strip() or None
        department = request.form.get("department", "").strip() or None

        if not name or not email or not password:
            flash("Name, email, and password are required.", "danger")
            return redirect(url_for("auth.register"))

        ok, result = auth_service.register_student(name, email, password, phone, department)
        if not ok:
            flash(result, "danger")
            return redirect(url_for("auth.register"))

        flash("Account created. Please sign in.", "success")
        return redirect(url_for("auth.student_login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def student_login():
    """Student login."""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = auth_service.authenticate(email, password, "student")
        if not user:
            flash("Invalid student credentials.", "danger")
            return redirect(url_for("auth.student_login"))

        session.clear()
        session.update(auth_service.build_session(user))
        flash("Welcome back to Study Sync!", "success")
        return redirect(url_for("student.dashboard"))

    return render_template("auth/login.html")


@auth_bp.route("/lecturer/login", methods=["GET", "POST"])
def lecturer_login():
    """Lecturer login."""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = auth_service.authenticate(email, password, "lecturer")
        if not user:
            flash("Invalid lecturer credentials.", "danger")
            return redirect(url_for("auth.lecturer_login"))

        session.clear()
        session.update(auth_service.build_session(user))
        flash("Lecturer portal unlocked.", "success")
        return redirect(url_for("lecturer.dashboard"))

    return render_template("auth/lecturer_login.html")


@auth_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Admin login."""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = auth_service.authenticate(email, password, "admin")
        if not user:
            flash("Invalid admin credentials.", "danger")
            return redirect(url_for("auth.admin_login"))

        session.clear()
        session.update(auth_service.build_session(user))
        flash("Admin access granted.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("auth/admin_login.html")


@auth_bp.route("/logout")
def logout():
    """Sign out and clear session."""
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("public.landing"))
