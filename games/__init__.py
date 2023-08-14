"""Initialize Flask app."""

from flask import Flask, render_template


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    with app.app_context():
        # Add blueprints here to register them.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .gamedesc import gamedesc
        app.register_blueprint(gamedesc.gamedesc_blueprint)

    return app
