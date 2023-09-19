import games.adapters.repository as repo


def get_user(username):
    user = repo.repo_instance.get_user(username)
    return user
