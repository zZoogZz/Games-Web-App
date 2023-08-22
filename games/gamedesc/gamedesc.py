from flask import Blueprint, render_template, abort
from games.domainmodel.model import Game
from games.utilities import utilities

import games.adapters.repository as repo


gamedesc_blueprint = Blueprint(
    'game_bp', __name__)


def get_game(game_id):
    game = repo.repo_instance.get_game(game_id)
    return game

@gamedesc_blueprint.route('/game/<int:game_id>')
def desc(game_id):
    some_game = get_game(game_id)
    if isinstance(some_game, Game):
        # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
        return render_template('gameDescription.html', game=some_game, top_genres=utilities.get_top_genres())
    else:
        return abort(404)