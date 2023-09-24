from flask import Blueprint, session

from games.authentication.authentication import login_required
from games.games_list._render_game_list import render_game_list
import games.games_list._services as services
import games.authentication.services as authservices


favourites_blueprint = Blueprint(
    'favourites_bp', __name__)


@favourites_blueprint.route('/games/list/favourites', methods=['GET'])
@login_required
def favourite_games():
    games = services.query_favourite_games()

    return render_game_list(games, "Favourites", errormessage="Look's like you don't have any favourites yet - add some!")