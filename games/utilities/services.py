from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game


def get_top_genres(repo: AbstractRepository):
    genres = repo.get_genres()
    genres = genres[:10]
    return genres


