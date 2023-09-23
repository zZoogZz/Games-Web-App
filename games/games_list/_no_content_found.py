from flask import render_template
from games.utilities import utilities


def no_content_found(header="Not Found", description="Hmmmm.... not sure what happened here. We didn't find anything."):
    return render_template('games/no_content_found.html', header=header, description=description, top_genres=utilities.get_top_genres())
