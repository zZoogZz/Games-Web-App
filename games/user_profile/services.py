import games.adapters.repository as repo


def get_user(username):
    user = repo.repo_instance.get_user(username)
    if user is not None:
        return user
    return None


def get_wishlists(user):
    pass