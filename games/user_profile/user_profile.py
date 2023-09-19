from flask import Blueprint, render_template, abort, session
from games.domainmodel.model import Game, User, Review
from games.utilities import utilities

import games.user_profile.services as services
from games.authentication.authentication import login_required

user_profile_blueprint = Blueprint(
    'user_profile_bp', __name__)


@user_profile_blueprint.route('/user_profile/')
@login_required
def user_profile():
    user_name = session['user_name']
    user = services.get_user(user_name)
    if isinstance(user, User):
        # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
        return render_template('user_profile/user_profile.html', user=user, top_genres=utilities.get_top_genres())
    else:
        return abort(404)