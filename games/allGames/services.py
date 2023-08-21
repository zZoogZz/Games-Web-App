from games.adapters.repository import AbstractRepository


def all_games_by_name(repo: AbstractRepository):
    game_ids_sorted = repo.get_game_ids_sorted_by_title()
    sorted_game_object_list = repo.get_games_by_ids(game_ids_sorted)
    return sorted_game_object_list
