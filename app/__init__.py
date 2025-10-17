from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from pathlib import Path
import os

# Global extensions

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Basic configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-change-me"),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL", f"sqlite:///{Path(app.instance_path) / 'app.db'}"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=True,
    )

    # Ensure instance folder exists
    try:
        Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"

    # Register blueprints
    from .auth.routes import auth_bp
    from .main.routes import main_bp
    from .courses.routes import courses_bp
    from .enrollments.routes import enrollments_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(courses_bp, url_prefix="/courses")
    app.register_blueprint(enrollments_bp, url_prefix="/enrollments")

    # CLI commands
    register_cli(app)

    return app


def register_cli(app: Flask) -> None:
    @app.cli.command("init-db")
    def init_db_command():
        """Initialize the database (create tables)."""
        from . import models  # noqa: F401 - ensure models are imported
        db.create_all()
        print("Initialized the database.")

    @app.cli.command("seed")
    def seed_command():
        """Seed initial data like admin user and demo classes."""
        from .seed import seed_data
        seed_data()
        print("Seeded initial data.")
