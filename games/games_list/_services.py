from flask import session
import games.adapters.repository as repository
from games.authentication.authentication import login_required
from games.games_list._public_services import toggle_favourite, get_favourites


def query_all_games_by_name(repo=repository) -> list:
    """
    Fetches all games, and returns them as a list.
    """

    game_ids_sorted = repo.repo_instance.get_game_ids_sorted_by_title()
    sorted_game_object_list = repo.repo_instance.get_games_by_ids(game_ids_sorted)

    return sorted_game_object_list


def query_games_title(query, repo=repository.repo_instance) -> list:
    """
    Takes a query string, compares with game title, and returns values where there is a substring.

    Returns a list of game objects.
    """
    sorted_game_object_list = query_all_games_by_name(repo)

    result = []

    for game in sorted_game_object_list:
        if query.lower() in game.title.lower():
            result.append(game)
    """
    if result == []:
        raise NoResultsFoundException(f"No games found for '{query}' in titles.")
    """
    return result


def query_publisher(query, repo=repository.repo_instance) -> list:
    """
    Takes a query string, compares with game title, and returns values where there is a substring.

    Returns a list of game objects.
    """
    sorted_game_object_list = query_all_games_by_name(repo)

    result = []

    for game in sorted_game_object_list:
        if query.lower() in game.publisher.publisher_name.lower():
            result.append(game)
    """
    if result == []:
        raise NoResultsFoundException(f"No games found for '{query}' in publishers.")
    """
    return result


def query_genre(query, repo=repository.repo_instance) -> list:

    sorted_game_object_list = query_all_games_by_name(repo)

    result = []

    for game in sorted_game_object_list:
        for genre in game.genres:
            if query.lower() in genre.genre_name.lower() and game not in result:
                result.append(game)
    """
    if result == []:
        raise NoResultsFoundException(f"No games found for '{query}' in genres.")
    """
    return result


@login_required
def query_favourite_games(repo=repository.repo_instance) -> list:
    """
    Retrieves all favourite games for the authorized user.

    Returns a list of game objects.
    """
    result = get_favourites()

    return result


def query_wishlist_games(wishlist_id,repo=repository.repo_instance) -> list:
    """
    Retrieves all wishlist games from a specified wishlist for the authorized user.

    Returns a list of game objects.
    """
    # TODO: link to memory repo
    result = []

    return result
