from flask import Blueprint
from games.games_list._render_game_list import render_game_list
import games.games_list._services as services

favourites_blueprint = Blueprint(
    'favourites_bp', __name__)


@favourites_blueprint.route('/games/list/favourites', methods=['GET'])
def favourite_games():

    games = services.query_favourite_games()

    return render_game_list(games, "Favourites")