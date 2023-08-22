from flask import Blueprint, request

from games.allGames.render_game_list import render_game_list
import games.allGames.services as services

games_search_blueprint = Blueprint(
    'search_bp', __name__)


@games_search_blueprint.route('/games/search', methods=['GET'])
def search_games():
    args = request.args
    query = args.get("query", default="", type=str)
    query_type = args.get("type", default="title", type=str)

    print(query_type)
    # Check the type of query that has been defined, and route accordingly.
    if query_type == "title":
        # Title Query
        games = services.query_games_title(query)
    elif query_type == "publisher":
        # Publisher Query
        games = services.query_publisher(query)
    elif query_type == "genre":
        # Genre Query
        games = services.query_genre(query)
    else:
        # If a type is defined but none are applicable, nothing is returned.
        games = []

    return render_game_list(games)


