"""Initialize Flask app."""

from pathlib import Path
from flask import Flask, render_template

import games.adapters.repository as repo
from games.adapters.memory_repository import MemoryRepository, populate

def create_app(test_config=None):
    """Construct the core application."""


    data_path = Path('games') / 'adapters' / 'data'

    # Create the Flask app object.
    app = Flask(__name__)

    app.config.from_object('config.Config')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        # data_path = app.config['TEST_DATA_PATH']

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

        from .allGames import allGames
        app.register_blueprint(allGames.all_games_blueprint)

        from .allGames import search
        app.register_blueprint(search.games_search_blueprint)

        from .errorHandlers import notFoundError
        app.register_blueprint(notFoundError.not_found_blueprint)
    return app


