from flask import Blueprint
from games.allGames.render_game_list import render_game_list
import games.allGames.services as services

all_games_blueprint = Blueprint(
    'all_games_bp', __name__)


@all_games_blueprint.route('/games/all', methods=['GET'])
def all_games():

    games = services.query_all_games_by_name()

    return render_game_list(games)
