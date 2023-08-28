from flask import render_template, Blueprint
from games.utilities import utilities

not_found_blueprint = Blueprint(
    'errorhandler_bp', __name__)


@not_found_blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', top_genres=utilities.get_top_genres()), 404
