from flask import Blueprint, render_template, abort
from games.domainmodel.model import Game, User, Review
from games.utilities import utilities

import games.user_profile.services as services
import games.adapters.repository as repo


user_profile_blueprint = Blueprint(
    'game_bp', __name__)




@user_profile_blueprint.route('/user_profile/<str:username>')
def user_profile(username):
    user = services.get_user(username)
    if isinstance(some_game, Game):
        # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
        return render_template('gameDescription.html', game=some_game, top_genres=utilities.get_top_genres())
    else:
        return abort(404)