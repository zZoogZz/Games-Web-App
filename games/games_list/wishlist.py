from flask import Blueprint
from games.games_list._render_game_list import render_game_list
import games.games_list._services as services

wishlist_blueprint = Blueprint(
    'wishlist_bp', __name__)


@wishlist_blueprint.route('/games/list/wishlist/', methods=['GET'])
def wishlist_list():
    raise NotImplementedError


@wishlist_blueprint.route('/games/list/wishlist/<int:wishlist_id>/', methods=['GET'])
def wishlist(wishlist_id):
    games = services.query_wishlist_games(wishlist_id)
    heading = "Wishlist: {}".format(wishlist_id)
    return render_game_list(games, heading, errormessage="Look's like you don't have any favourites yet - add some!")
