import os

from flask import Flask

from app.extensions import db, socketio
from configuration import DATABASE_PATH, Configuration


def create_app(config_class=Configuration):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app)

    # Register blueprints
    from app.chat import bp as chat_bp

    app.register_blueprint(chat_bp)

    # Create database models if not exists
    if not os.path.exists(DATABASE_PATH):
        with app.app_context():
            db.create_all()

    return app
