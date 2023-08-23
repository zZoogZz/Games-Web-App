from flask import render_template, Blueprint

not_found_blueprint = Blueprint(
    'errorhandler_bp', __name__)


@not_found_blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
