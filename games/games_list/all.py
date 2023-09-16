from flask import Blueprint
from games.games_list._render_game_list import render_game_list
import games.games_list._services as services

all_blueprint = Blueprint(
    'all_games_bp', __name__)


@all_blueprint.route('/games/all', methods=['GET'])
def all_games():

    games = services.query_all_games_by_name()

    return render_game_list(games, "All Games")
