from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config=None):
    """Application factory: makes the app easy to configure and test."""
    app = Flask(__name__, static_folder="static")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobs.db"
    if config:
        app.config.update(config)

    db.init_app(app)

    from .routes import bp

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()
    return app
