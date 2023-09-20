from flask import Blueprint, render_template, abort, session, request
from games.domainmodel.model import Game, User, Review
from games.utilities import utilities
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField

import games.user_profile.services as services
from games.authentication.authentication import login_required

user_profile_blueprint = Blueprint(
    'user_profile_bp', __name__)


@user_profile_blueprint.route('/user_profile/')
@login_required
def user_profile():
    user_name = session['user_name']
    user = services.get_user(user_name)

    sort_choice = request.args.get('sort_choice', default='Highest Rating')

    sorting = Sorting(sort_choice=sort_choice)

    if sorting.validate_on_submit():
        sort_choice = sorting.sort_choice.data

    sorted_reviews = sort_reviews(user, sort_choice)

    # dummy favourites:
    # import games.adapters.repository as repo
    # user.add_favourite_game(repo.repo_instance.get_game(410320))
    # user.add_favourite_game(repo.repo_instance.get_game(730310))
    # user.add_favourite_game(repo.repo_instance.get_game(1271620))
    # user.add_favourite_game(repo.repo_instance.get_game(1022480))
    # user.add_favourite_game(repo.repo_instance.get_game(299380))
    # user.add_favourite_game(repo.repo_instance.get_game(441670))
    # end dummy favourites

    # wishlists = services.get_wishlists(user)

    if isinstance(user, User):
        # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
        return render_template('user_profile/user_profile.html',
                               user=user,
                               top_genres=utilities.get_top_genres(),
                               sorting=sorting,
                               sort_choice=sort_choice,
                               sorted_reviews=sorted_reviews)
    else:
        return abort(404)


class Sorting(FlaskForm):
    sort_choice = SelectField('Sort By', choices=['Highest Rating', 'Lowest Rating', 'Game A-Z', 'Game Z-A'])
    submit = SubmitField('Sort')


def sort_reviews(user, sort_choice):
    if sort_choice == 'Highest Rating':
        sort_by = 'rating'
        reverse_sort = True
    elif sort_choice == 'Lowest Rating':
        sort_by = 'rating'
        reverse_sort = False
    elif sort_choice == 'Game A-Z':
        sort_by = 'game'
        reverse_sort = False
    else: # sort_choice == 'User Z-A':
        sort_by = 'game'
        reverse_sort = True

    if sort_by == 'rating':
        return sorted(user.reviews, key=lambda review: review.rating, reverse=reverse_sort)
    else:
        return sorted(user.reviews, key=lambda review: review.game.title.lower(), reverse=reverse_sort)