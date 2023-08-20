from flask import Blueprint, render_template

nav_blueprint = Blueprint('nav_bp', __name__)

@home_blueprint.route('/')
def nav():
    return render_template('navigation.html')