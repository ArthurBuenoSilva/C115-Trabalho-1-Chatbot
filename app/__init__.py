from flask import Flask

from configuration import Configuration

def create_app(config_class=Configuration):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions

    # Register blueprints
    from app.chat import bp as chat_bp
    app.register_blueprint(chat_bp)

    return app