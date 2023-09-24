from flask import session
import games.adapters.repository as repo
from games.authentication.authentication import login_required


@login_required
def toggle_favourite(game, repo=repo):
    """
    Toggles the games status as a favourite.
    """
    user = repo.repo_instance.get_user(session['user_name'])

    repo.repo_instance.toggle_favourite(game, user)


def toggle_wishlist(game, repo):
    """
    Toggles the games status on a wishlist.
    """
    raise NotImplementedError


def is_favourite(game, repo=repo):
    user = repo.repo_instance.get_user(session['user_name'])
    if user is None:
        return False
    else:
        return repo.repo_instance.game_is_favourite(game, user)


def get_favourites(repo=repo):
    if 'user_name' not in session:
        return []

    user = repo.repo_instance.get_user(session['user_name'])

    if user is None:
        return []

    return repo.repo_instance.get_favourites(user)
