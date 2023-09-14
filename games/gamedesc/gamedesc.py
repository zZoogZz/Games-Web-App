from games.domainmodel.model import Game, User, Review
from games.utilities import utilities

from flask import session
from flask import Blueprint, render_template, abort, url_for, request, redirect

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

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
    if isinstance(some_game, Game):
        # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
        return render_template('gameDescription.html', game=some_game, top_genres=utilities.get_top_genres())
    else:
        return abort(404)

@gamedesc_blueprint.route('/review', methods=['GET', 'POST'])
# @login_required
def review_game():
    user = {
        'user_name': 'a_user',
        'password': 'a_password'
    }
    repo.repo_instance.add_user(User(user['user_name'], user['password']))

    session.clear()
    session['user_name'] = user['user_name']
    user_name = session['user_name']

    form = ReviewForm()

    if form.validate_on_submit():

        game_id = int(form.game_id.data)
        services.add_review(user_name, game_id, int(form.rating.data), form.review.data, repo.repo_instance)

        # game = services.get_game(game_id, repo.repo_instance)

        return redirect(url_for('game_bp.desc', game_id=game_id))


    if request.method == 'GET':
        game_id = int(request.args.get('game'))

        form.game_id.data = game_id
    else:
        game_id = int(form.game_id.data)

    game = services.get_game(game_id, repo.repo_instance)


    return render_template(
        'games/review_game.html',
        game=game,
        form=form,
        handler_url=url_for('game_bp.review_game', game=game_id),
        top_genres=utilities.get_top_genres(),
        # sort_by='rating',
        # sort_reverse=True
        # selected_articles=utilities.get_selected_games(),
        # tag_urls=utilities.get_tags_and_urls()
    )


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short')])
    game_id = HiddenField("Game ID")
    rating = SelectField('Rating', choices=[0, 1, 2, 3, 4, 5])
    submit = SubmitField('Submit')



