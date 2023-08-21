from games.adapters.repository import AbstractRepository
from operator import itemgetter

def get_top_genres(repo: AbstractRepository, number_to_get):
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


