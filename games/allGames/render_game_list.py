from games.utilities import utilities
from flask import render_template, request
import games.allGames.services as services
#
# TODO IMPLEMENT PAGINATION
#
def render_game_list(game_list):
    """
    Takes a list of games and paginates then renders the output.
    """
    page = request.args.get('page', 1, type=int)
    games_per_page = 20
    start_index = (page - 1) * games_per_page
    end_index = start_index + games_per_page
    paginated_games = game_list[start_index:end_index]
    total_games = len(game_list)
    total_game_pages = (total_games + games_per_page - 1) // games_per_page
    return render_template('games/games.html', all_games=paginated_games, top_genres=utilities.get_top_genres(), page=page, total_game_pages=total_game_pages)