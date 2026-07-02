"""Seed lecturer and admin accounts with secure password hashes.

Usage:
    python scripts/seed_users.py
"""

from werkzeug.security import generate_password_hash

LECTURER_EMAIL = "lecturer@studysync.app"
LECTURER_PASSWORD = "lecturer123"
ADMIN_EMAIL = "admin@studysync.app"
ADMIN_PASSWORD = "admin123"

if __name__ == "__main__":
    print("-- Run these SQL updates after importing database.sql --")
    print()
    print(f"Lecturer ({LECTURER_EMAIL} / {LECTURER_PASSWORD}):")
    print(f"  {generate_password_hash(LECTURER_PASSWORD)}")
    print()
    print(f"Admin ({ADMIN_EMAIL} / {ADMIN_PASSWORD}):")
    print(f"  {generate_password_hash(ADMIN_PASSWORD)}")
    print()
    print("UPDATE users SET password_hash='<hash>' WHERE email='lecturer@studysync.app';")
    print("UPDATE users SET password_hash='<hash>' WHERE email='admin@studysync.app';")
