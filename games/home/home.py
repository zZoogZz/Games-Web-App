import flask
from flask import Blueprint, render_template, request, url_for

import games.utilities.utilities as utilities

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template('home/home.html', top_genres=utilities.get_top_genres())


@home_blueprint.route('/', methods=['POST'])
def home_search_post():
    query = request.form['query']
    query_type = "title"

    return flask.redirect(url_for("search_bp.search_games", query=query, query_type=query_type))