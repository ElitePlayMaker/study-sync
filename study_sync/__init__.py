"""Study Sync — Flask application factory."""

from datetime import datetime

from dotenv import load_dotenv
from flask import Flask

from study_sync.config import Config
from study_sync.controllers.admin import admin_bp
from study_sync.controllers.auth import auth_bp
from study_sync.controllers.lecturer import lecturer_bp
from study_sync.controllers.public import public_bp
from study_sync.controllers.student import student_bp
from study_sync.extensions import close_db

load_dotenv()


def create_app(config_class=Config):
    """Create and configure the Study Sync Flask application."""
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_object(config_class)

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(lecturer_bp)
    app.register_blueprint(admin_bp)

    app.teardown_appcontext(close_db)

    @app.context_processor
    def inject_globals():
        """Expose brand constants to all templates."""
        return {
            "APP_NAME": app.config["APP_NAME"],
            "APP_TAGLINE": app.config["APP_TAGLINE"],
            "current_year": datetime.now().year,
        }

    return app
