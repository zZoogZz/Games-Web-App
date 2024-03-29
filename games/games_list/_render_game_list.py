from games.games_list._no_content_found import no_content_found
from games.utilities import utilities
from flask import render_template, request, redirect, url_for, abort
import games.games_list._services as services

GAMES_PER_PAGE = 20


def render_game_list(game_list, heading="List name not found.", errormessage="Hmmm..... We couldn't find anything....."):
    """
    Takes a list of games and paginates then renders the output.
    """

    if len(game_list) < 1: return no_content_found(header=heading,
                                                   description="Hmmm..... We couldn't find anything.....")

    page = request.args.get('page', 1, type=int)  # Gets page number

    search_query = request.args.get('query')
    search_query_type = request.args.get('query_type')

    start_index = (page - 1) * GAMES_PER_PAGE
    end_index = start_index + GAMES_PER_PAGE
    paginated_games = game_list[start_index:end_index]
    total_games = len(game_list)
    total_game_pages = (total_games + GAMES_PER_PAGE - 1) // GAMES_PER_PAGE

    return render_template('games/games.html', all_games=paginated_games, top_genres=utilities.get_top_genres(),
                           page=page, total_game_pages=total_game_pages, heading=heading, search_query=search_query, search_query_type=search_query_type)
