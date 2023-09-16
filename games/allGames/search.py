from flask import Blueprint, request, render_template
from games.errorHandlers.custom_exceptions import NoResultsFoundException
from games.allGames.render_game_list import render_game_list
import games.allGames.services as services
from games.utilities import utilities

games_search_blueprint = Blueprint(
    'search_bp', __name__)


@games_search_blueprint.route('/games/search', methods=['GET'])
def search_games():
    args = request.args
    query = args.get("query", default="", type=str)
    query_type = args.get("query_type", default="title", type=str)
    # Check the type of query that has been defined, and route accordingly.
    try:
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
        heading = "Showing results for {} search of \"{}\"....".format(query_type, query)
        return render_game_list(games, heading=heading)
    except NoResultsFoundException as message:
        # TODO: Move no results error to render_game_list to render for all lists.
        return render_template('errors/no_results.html', message=message,
                               top_genres=utilities.get_top_genres())



