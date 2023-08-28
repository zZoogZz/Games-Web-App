from games.adapters.repository import AbstractRepository
from operator import itemgetter
from typing import List


def get_top_genres(repo: AbstractRepository, number_to_get) -> List[tuple]:
    if not isinstance(repo, AbstractRepository) or not isinstance(number_to_get, int):
        return []
    games = repo.get_games()
    genre_count = dict()
    for game in games.values():
        genres = game.genres
        for genre in genres:
            if genre not in genre_count:
                genre_count[genre] = 1
            else:
                genre_count[genre] += 1
    top_genres = sorted(genre_count.items(), key=itemgetter(1), reverse=True)[:number_to_get]  # as list of tuples

    return top_genres


