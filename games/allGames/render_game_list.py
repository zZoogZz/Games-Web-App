from games.utilities import utilities
from flask import render_template

#
# TODO IMPLEMENT PAGINATION
#


def render_game_list(game_list):
    """
    Takes a list of games and paginates then renders the output.
    """

    return render_template('games/games.html', all_games=game_list, top_genres=utilities.get_top_genres())