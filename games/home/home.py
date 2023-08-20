from flask import Blueprint, render_template

import games.utilities.utilities as utilities

home_blueprint = Blueprint(
    'home_bp', __name__)

print('home')

@home_blueprint.route('/', methods=['GET'])
def home():
    print('home route')
    return render_template('home/home.html',
                           top_genres=utilities.get_top_genres()                           )