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

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    print(data_path)

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # fill repository with the content from the provided csv files
    populate(repo.repo_instance, data_path)

    with app.app_context():
        # Add blueprints here to register them.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .gamedesc import gamedesc
        app.register_blueprint(gamedesc.gamedesc_blueprint)

        from .games_list import all, search, favourites, wishlist
        app.register_blueprint(all.all_blueprint)
        app.register_blueprint(search.search_blueprint)
        app.register_blueprint(favourites.favourites_blueprint)
        app.register_blueprint(wishlist.wishlist_blueprint)

        from .errorHandlers import error_handler
        app.register_blueprint(error_handler.error_handler_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .user_profile import user_profile
        app.register_blueprint(user_profile.user_profile_blueprint)

    return app


