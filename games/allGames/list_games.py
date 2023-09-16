from flask import Blueprint
from games.allGames.render_game_list import render_game_list
import games.allGames.services as services

list_games_blueprint = Blueprint(
    'list_games_bp', __name__)


@list_games_blueprint.route('/games/list/favourite', methods=['GET'])
def favourite_games():
    # games = services.query_all_games_by_name()
    # games = services.query_favourite_games()
    games = []

    return render_game_list(games, "Favourites")


@list_games_blueprint.route('/games/list/wishlist/', methods=['GET'])
def wishlist_list():
    # games = services.query_all_games_by_name()
    #games = services.query_favourite_games()

    games = []
    return render_game_list(games, "Wishlist")


@list_games_blueprint.route('/games/list/wishlist/1/', methods=['GET'])
def wishlist():
    # games = services.query_all_games_by_name()
    #games = services.query_favourite_games()
    games = []

    return render_game_list(games, "Wishlist 1")
