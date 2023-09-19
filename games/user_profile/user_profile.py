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
    print(user)

    # dummy favourites:
    # import games.adapters.repository as repo
    # user.add_favourite_game(repo.repo_instance.get_game(410320))
    # user.add_favourite_game(repo.repo_instance.get_game(730310))
    # user.add_favourite_game(repo.repo_instance.get_game(1271620))
    # user.add_favourite_game(repo.repo_instance.get_game(1022480))
    # user.add_favourite_game(repo.repo_instance.get_game(299380))
    # user.add_favourite_game(repo.repo_instance.get_game(441670))
    # end dummy favourites

    # wishlists = servieces.get_wishlists(user)
    if isinstance(user, User):
        # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
        return render_template('user_profile/user_profile.html', user=user, top_genres=utilities.get_top_genres())
    else:
        return abort(404)