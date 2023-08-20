from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import Game
# from games.adapters.repository import AbstractRepository


def get_top_genres(repo):
    genres = repo.get_genres()
    genres = genres[:10]
    return genres


