from flask import Blueprint, request
from games.games_list._render_game_list import render_game_list
import games.games_list._services as services

search_blueprint = Blueprint(
    'search_bp', __name__)


@search_blueprint.route('/games/search', methods=['GET'])
def search_games():
    """
    A GET method, pulls the type of search from the URL, and routes to the appropriate query method.

    The renderer then paginates and handles empty list situations.
    """
    # Initialization - Fetching Args.

    args = request.args
    query = args.get("query", default="", type=str)
    query_type = args.get("query_type", default="title", type=str)

    # Query Check - Check the type of query that has been defined, and route accordingly.

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

    # Render

    print(type(games))

    heading = query

    return render_game_list(games, heading=heading)



