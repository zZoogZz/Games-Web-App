from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from games.domainmodel.model import Game
from games.utilities import utilities

import games.adapters.repository as repo
import games.allGames.services as services

all_games_blueprint = Blueprint(
    'all_games_bp', __name__)

def all_games_by_name():
    # Returns list of all game objects from CSV file in alphabetical order
    all_games = services.all_games_by_name(repo.repo_instance)
    return all_games

@all_games_blueprint.route('/all_games', methods=['GET'])
def all_games():
        all_games = all_games_by_name()
        # Use Jinja to customize a predefined html page rendering the layout for all games in alphabetical order
        return render_template('allGames.html', all_games=all_games, top_genres=utilities.get_top_genres())


