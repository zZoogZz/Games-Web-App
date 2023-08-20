from flask import Blueprint, render_template, url_for

import games.adapters.repository as repo

import games.utilities.services as services

utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_top_genres():
    top_genres = services.get_top_genres(repo.repo_instance, 10)
    return top_genres


