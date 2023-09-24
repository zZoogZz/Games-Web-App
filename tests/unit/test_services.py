import pytest
import os
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.adapters.memory_repository import MemoryRepository, populate
import games.adapters.repository as repo
import games.utilities.services as services
import games.utilities.utilities as utilities
import games.games_list._services as allGamesServices


# Utilities tests:
def test_get_top_genres():

    repo.repo_instance = MemoryRepository()

    genres0 = services.get_top_genres(repo.repo_instance, 10)
    assert genres0 == []

    populate(repo.repo_instance, "./games/adapters/data/")
    genres0 = services.get_top_genres(repo.repo_instance, 0)
    assert genres0 == []
    genres0 = services.get_top_genres(repo.repo_instance, 1)
    assert genres0 == [(Genre("Indie"), 649)]
    assert genres0 == [(Genre("Indie"), 649)]
    genres0 = services.get_top_genres(repo.repo_instance, 10)
    assert genres0[-2:] == [(Genre("Free to Play"), 65),(Genre("Sports"), 41)]
    genres0 = services.get_top_genres(repo.repo_instance, "five")
    assert genres0 == []
    genres0 = services.get_top_genres("not a repo", 10)
    assert genres0 == []
    genres0 = services.get_top_genres(repo.repo_instance, 1000)
    assert len(genres0) == 24

# games_list tests:

def test_query_all_games_by_name():
    repo.repo_instance = MemoryRepository()
    allGames0 = allGamesServices.query_all_games_by_name(repo)
    assert allGames0 == []  # check list begins empty before populate is called
    populate(repo.repo_instance, "./games/adapters/data/")
    allGames1 = allGamesServices.query_all_games_by_name(repo)
    assert allGames1 != []  # check populate works
    for i in range(len(allGames1) - 1):
        assert allGames1[i].title < allGames1[i+1].title  # check all games are in order by title


def test_query_games_title():
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance, "./games/adapters/data/")
    allGames = allGamesServices.query_all_games_by_name(repo)
    searched_games0 = allGamesServices.query_games_title("The", repo)
    assert searched_games0 != []  # checks that it returns items to the list
    for game in searched_games0:
        assert "the" in game.title.lower()  # checks that all items actually contain "the"
    searched_games1 = allGamesServices.query_games_title("", repo)
    assert len(searched_games1) == len(allGames)  # defaults to all games



def test_query_publisher():
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance, "./games/adapters/data/")
    allGames = allGamesServices.query_all_games_by_name(repo)
    searched_publishers0 = allGamesServices.query_publisher("a", repo)
    assert searched_publishers0 != []  # checks that it returns items to the list
    for game in searched_publishers0:
        assert "a" in game.publisher.publisher_name.lower()  # checks that all items actually contain "a"
    searched_publishers1 = allGamesServices.query_publisher("", repo)
    assert len(searched_publishers1) == len(allGames)  # defaults to all games


def test_query_genres():
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance, "./games/adapters/data/")
    search_term = "Adventure"
    allGames = allGamesServices.query_all_games_by_name(repo)
    searched_genres0 = allGamesServices.query_genre(search_term, repo)
    assert searched_genres0 != []  # checks that it returns items to the list
    for game in searched_genres0:
        genre_list = []
        counter = 0
        for genre in game.genres:
            genre_list.append(genre.genre_name.lower())
        for genre in genre_list:
            if search_term.lower() in genre:
                counter += 1
        assert counter > 0
    searched_genres1 = allGamesServices.query_genre("", repo)
    assert len(searched_genres1) == len(allGames)  # defaults to all games







