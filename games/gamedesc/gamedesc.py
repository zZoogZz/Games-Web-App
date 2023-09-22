from games.domainmodel.model import Game, User, Review
from games.utilities import utilities

from flask import session
from flask import Blueprint, render_template, abort, url_for, request, redirect

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from games.authentication.authentication import login_required

import games.adapters.repository as repo
import games.gamedesc.services as services

gamedesc_blueprint = Blueprint(
    'game_bp', __name__)


def get_game(game_id):
    game = repo.repo_instance.get_game(game_id)
    return game

@gamedesc_blueprint.route('/game/<int:game_id>')
def desc(game_id):
    some_game = get_game(game_id)
    if not isinstance(some_game, Game):
        return abort(404)

    # Get sorting choices:
    sort_choice = request.args.get('sort_choice', default='Highest Rating')

    sorting = Sorting(sort_choice=sort_choice)

    if sorting.validate_on_submit():
        sort_choice = sorting.sort_choice.data

    sorted_reviews = sort_reviews(some_game, sort_choice)

    already_reviewed = services.get_existing_review(some_game) is not None

    # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
    return render_template('gameDescription.html',
                           game=some_game,
                           top_genres=utilities.get_top_genres(),
                           sorted_reviews=sorted_reviews,
                           sorting=sorting,
                           sort_choice=sort_choice,
                           already_reviewed=already_reviewed
                           )

@gamedesc_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_game():
    user_name = session['user_name']

    form = ReviewForm()

    # maintain sorting choices:
    sort_choice = request.args.get('sort_choice', default='Highest Rating')

    game_id = int(request.args.get('game', default=form.game_id.data))
    form.game_id.data = game_id
    some_game = services.get_game(game_id, repo.repo_instance)

    existing_review = services.get_existing_review(some_game)
    already_reviewed = existing_review is not None
    if already_reviewed:
        form = ReviewForm(review=existing_review.comment, rating=existing_review.rating)

    if form.validate_on_submit():

        # game_id = int(form.game_id.data)
        services.add_review(user_name, game_id, int(form.rating.data), form.review.data, repo.repo_instance)

        return redirect(url_for('game_bp.desc', game_id=game_id, sort_choice=sort_choice))

    return render_template(
        'games/review_game.html',
        game=some_game,
        form=form,
        handler_url=url_for('game_bp.review_game', game=game_id, sort_choice=sort_choice),
        top_genres=utilities.get_top_genres(),
        sort_choice=sort_choice
    )


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short')])
    game_id = HiddenField("Game ID")
    rating = SelectField('Rating', choices=[0, 1, 2, 3, 4, 5])
    submit = SubmitField('Submit')


class Sorting(FlaskForm):
    sort_choice = SelectField('Sort By', choices=['Highest Rating', 'Lowest Rating', 'User A-Z', 'User Z-A'])
    submit = SubmitField('Sort')


def sort_reviews(game, sort_choice):
    if sort_choice == 'Highest Rating':
        sort_by = 'rating'
        reverse_sort = True
    elif sort_choice == 'Lowest Rating':
        sort_by = 'rating'
        reverse_sort = False
    elif sort_choice == 'User A-Z':
        sort_by = 'user'
        reverse_sort = False
    else: # sort_choice == 'User Z-A':
        sort_by = 'user'
        reverse_sort = True

    if sort_by == 'rating':
        return sorted(game.reviews, key=lambda review: review.rating, reverse=reverse_sort)
    else:
        return sorted(game.reviews, key=lambda review: review.user.username.lower(), reverse=reverse_sort)
