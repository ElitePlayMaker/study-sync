"""Database connection helpers for request-scoped MySQL access."""

import mysql.connector
from flask import current_app, g


def get_db():
    """Return a single MySQL connection per request."""
    if "db" not in g:
        g.db = mysql.connector.connect(
            host=current_app.config["DB_HOST"],
            port=current_app.config["DB_PORT"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            database=current_app.config["DB_NAME"],
            autocommit=False,
        )
    return g.db


def close_db(_exception=None):
    """Close the database connection at the end of a request."""
    db = g.pop("db", None)
    if db is not None and db.is_connected():
        db.close()
