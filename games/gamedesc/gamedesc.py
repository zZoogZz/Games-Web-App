from flask import Blueprint, render_template
from games.domainmodel.model import Game

gamedesc_blueprint = Blueprint(
    'game_bp', __name__)

# TODO: Access to the games should be implemented via the repository pattern, so this can not stay here!

def create_some_game():
    some_game = Game(1, "Call of Duty® 4: Modern Warfare®")
    some_game.release_date = "Nov 12, 2007"
    some_game.price = 9.99
    some_game.description = "The new action-thriller from the award-winning team at Infinity Ward, the creators of " \
                            "the Call of Duty® series, delivers the most intense and cinematic action experience ever. "
    some_game.image_url = "https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118"
    return some_game

@gamedesc_blueprint.route('/desc/')
def desc():
    some_game = create_some_game()
    # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
    return render_template('gameDescription.html', game=some_game)