from games.domainmodel.model import Game, User, Review
from games.utilities import utilities
from games.games_list._public_services import is_favourite, get_favourites

from flask import session
from flask import Blueprint, render_template, abort, url_for, request, redirect

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from games.authentication.authentication import login_required

import games.adapters.repository as repo
import games.gamedesc.services as services

from games.games_list._public_services import toggle_favourite, toggle_wishlist

gamedesc_blueprint = Blueprint(
    'game_bp', __name__)


def get_game(game_id):
    game = repo.repo_instance.get_game(game_id)
    return game


@login_required
@gamedesc_blueprint.route('/game/<int:game_id>',  methods=['GET', 'POST'])
def desc(game_id):
    if request.method == 'GET':
        some_game = get_game(game_id)
        if not isinstance(some_game, Game):
            return abort(404)

        sort_by = request.args.get('sort_by', default='rating')
        reverse_sort = request.args.get('reverse_sort', default='True') == 'True'

        sorting = Sorting()
        print('sorting made')

        if sorting.validate_on_submit():

            sort_by = sorting.sort_by.data
            reverse_sort = sorting.reverse_sort
            print(f'sort by: {sort_by}, reverse_sort: {reverse_sort}')

        sorted_reviews = sorted(some_game.reviews, key=lambda review: getattr(review, sort_by), reverse=reverse_sort)

        favourite_games = get_favourites()

        # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
        return render_template('/game/gameDescription.html',
                               game=some_game,
                               top_genres=utilities.get_top_genres(),
                               sorted_reviews=sorted_reviews,
                               sorting=sorting,
                               sort_by=sort_by,
                               reverse_sort=reverse_sort,
                               favourites=favourite_games
                               )
    elif request.method == 'POST':
        """
        When a post request is placed, this function triggers the associated toggle button function
        toggle_favourite
        toggle_wishlist
        """

        game = get_game(game_id)

        sort_by = request.args.get('sort_by', default='rating')
        reverse_sort = request.args.get('reverse_sort', default='True') == 'True'

        if request.form['submit_button'] == 'toggle_favourite':

            toggle_favourite(game)
            return redirect(url_for('game_bp.desc', game_id=game_id, sort_by=sort_by, reverse_sort=reverse_sort))
        elif request.form['submit_button'] == 'toggle_wishlist':
            # toggle_wishlist(game)
            # TODO re-enable wishlist
            print("toggling wishlist")
            pass
            return "Toggled WL"
        else:
            pass  # unknown


@gamedesc_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_game():
    # start authentication fudge:
    # user = {'user_name': 'a_user' + str(random.randint(0,5)), 'password': 'a_password'}
    # repo.repo_instance.add_user(User(user['user_name'], user['password']))
    # session.clear()
    # session['user_name'] = user['user_name']
    # user_name = session['user_name']
    # end authentication fudge

    user_name = session['user_name']

    form = ReviewForm()

    sort_by = request.args.get('sort_by', default='rating')
    reverse_sort = request.args.get('reverse_sort', default='True') == 'True'

    if form.validate_on_submit():

        game_id = int(form.game_id.data)
        services.add_review(user_name, game_id, int(form.rating.data), form.review.data, repo.repo_instance)

        # game = services.get_game(game_id, repo.repo_instance)

        return redirect(url_for('game_bp.desc', game_id=game_id, sort_by=sort_by, reverse_sort=reverse_sort))

    game_id = int(request.args.get('game', default=form.game_id.data))
    form.game_id.data = game_id

    game = services.get_game(game_id, repo.repo_instance)

    return render_template(
        'games/review_game.html',
        game=game,
        form=form,
        handler_url=url_for('game_bp.review_game', game=game_id, sort_by=sort_by, reverse_sort=reverse_sort),
        top_genres=utilities.get_top_genres()
    )


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short')])
    game_id = HiddenField("Game ID")
    rating = SelectField('Rating', choices=[0, 1, 2, 3, 4, 5])
    submit = SubmitField('Submit')


class Sorting(FlaskForm):
    sort_by = SelectField('Sort By', choices=['rating', 'user', 'date'])
    reverse_sort = SelectField('Order', choices=['True', 'False'])
    submit = SubmitField('Sort')


@gamedesc_blueprint.route('/', methods=['POST'])
def home_search_post():
    query = request.form['query']
    query_type = request.form['type']

    return redirect(url_for("search_bp.search_games", query=query, type=query_type))
