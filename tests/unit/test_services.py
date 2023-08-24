import pytest
import os
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.adapters.memory_repository import MemoryRepository, populate
import games.adapters.repository as repo
import games.utilities.services as services
import games.utilities.utilities as utilities


# Utilities tests:
def test_get_top_genres():

    repo.repo_instance = MemoryRepository()

    genres0 = services.get_top_genres(repo.repo_instance, 10)
    assert genres0 == []

    populate(repo.repo_instance)
    genres0 = services.get_top_genres(repo.repo_instance, 0)
    assert genres0 == []
    genres0 = services.get_top_genres(repo.repo_instance, 1)
    assert genres0 == [(Genre("Indie"), 649)]
    genres0 = services.get_top_genres(repo.repo_instance, 10)
    assert genres0[-2:] == [(Genre("Free to Play"), 65),(Genre("Sports"), 41)]
    genres0 = services.get_top_genres(repo.repo_instance, "five")
    assert genres0 == []
    genres0 = services.get_top_genres("not a repo", 10)
    assert genres0 == []
    genres0 = services.get_top_genres(repo.repo_instance, 1000)
    assert len(genres0) == 24


