from flask import Blueprint, render_template, url_for

import games.adapters.repository as repo

import games.utilities.services as services

utilities_blueprint = Blueprint(
    'utilities_bp', __name__)
print('utitlies main')
def get_top_genres():
    print('utilities get_top_genres')
    genres = services.get_top_genres(repo.repo_instance)
    return genres

