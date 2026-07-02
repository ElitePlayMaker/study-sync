"""Public routes — landing and contact pages."""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from study_sync.models import contact as contact_model
from study_sync.utils.email import send_contact_acknowledgement

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def landing():
    """Study Sync marketing landing page."""
    if session.get("role") == "student":
        return redirect(url_for("student.dashboard"))
    if session.get("role") == "lecturer":
        return redirect(url_for("lecturer.dashboard"))
    if session.get("role") == "admin":
        return redirect(url_for("admin.dashboard"))
    return render_template("public/landing.html")


@public_bp.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact page with form submission."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if not all([name, email, subject, message]):
            flash("Please complete all fields.", "danger")
            return redirect(url_for("public.contact"))

        contact_model.create(name, email, subject, message)
        send_contact_acknowledgement(name, email)
        flash("Thanks for reaching out. We will respond shortly.", "success")
        return redirect(url_for("public.contact"))

    return render_template("public/contact.html")
