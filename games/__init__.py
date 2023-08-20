"""Initialize Flask app."""

from pathlib import Path
from flask import Flask, render_template

import games.adapters.repository as repo
from games.adapters.memory_repository import MemoryRepository, populate

def create_app():
    """Construct the core application."""

    data_path = Path('games') / 'adapters' / 'data'

    # Create the Flask app object.
    app = Flask(__name__)

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # fill repository with the content from the provided csv files
    populate(repo.repo_instance)


    with app.app_context():
        # Add blueprints here to register them.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .gamedesc import gamedesc
        app.register_blueprint(gamedesc.gamedesc_blueprint)

    return app


