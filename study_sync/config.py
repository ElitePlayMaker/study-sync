import os


class Config:
    """Application configuration loaded from environment variables."""

    SECRET_KEY = os.getenv("SECRET_KEY", "study-sync-dev-secret-change-in-production")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "study_sync")

    MAIL_ENABLED = os.getenv("MAIL_ENABLED", "false").lower() == "true"
    MAIL_FROM = os.getenv("MAIL_FROM", "noreply@studysync.app")
    APP_NAME = "Study Sync"
    APP_TAGLINE = "Learn Together. Schedule Smarter."
