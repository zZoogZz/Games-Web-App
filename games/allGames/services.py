from games.adapters.repository import AbstractRepository
import games.adapters.repository as repository
from games.errorHandlers.custom_exceptions import NoResultsFoundException

def query_all_games_by_name(repo=repository.repo_instance):
    game_ids_sorted = repo.get_game_ids_sorted_by_title()
    sorted_game_object_list = repo.get_games_by_ids(game_ids_sorted)
    return sorted_game_object_list


def query_games_title(query, repo=repository.repo_instance):
    """
    Takes a query string, compares with game title, and returns values where there is a substring.

    Returns a list of game objects.
    """
    sorted_game_object_list = query_all_games_by_name(repo)

    result = []

    for game in sorted_game_object_list:
        if query.lower() in game.title.lower():
            result.append(game)
    if result == []:
        raise NoResultsFoundException(f"No games found for '{query}' in titles.")
    return result


def query_publisher(query, repo=repository.repo_instance):
    """
    Takes a query string, compares with game title, and returns values where there is a substring.

    Returns a list of game objects.
    """
    sorted_game_object_list = query_all_games_by_name(repo)

    result = []

    for game in sorted_game_object_list:
        if query.lower() in game.publisher.publisher_name.lower():
            result.append(game)
    if result == []:
        raise NoResultsFoundException(f"No games found for '{query}' in publishers.")
    return result


def query_genre(query, repo=repository.repo_instance):

    sorted_game_object_list = query_all_games_by_name(repo)

    result = []

    for game in sorted_game_object_list:
        for genre in game.genres:
            if query.lower() in genre.genre_name.lower() and game not in result:
                result.append(game)
    if result == []:
        raise NoResultsFoundException(f"No games found for '{query}' in genres.")
    return result
