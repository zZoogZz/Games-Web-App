from flask import session
import games.adapters.repository as repo
from games.authentication.authentication import login_required


@login_required
def toggle_favourite(game, repo=repo):
    """
    Toggles the games status as a favourite.
    """
    user = repo.repo_instance.get_user(session['user_name'])

    if game in user.favourite_games:
        user.remove_favourite_game(game)
    else:
        user.add_favourite_game(game)


def toggle_wishlist(game, repo):
    """
    Toggles the games status on a wishlist.
    """
    raise NotImplementedError


def is_favourite(game, repo=repo):
    user = repo.repo_instance.get_user(session['user_name'])
    if user is None:
        return False

    if game in user.favourite_games:
        return True
    else:
        return False


def get_favourites(repo=repo):
    if 'user_name' not in session:
        return []

    user = repo.repo_instance.get_user(session['user_name'])

    if user is None:
        return []

    return user.favourite_games
