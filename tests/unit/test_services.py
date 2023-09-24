import pytest
import os
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.adapters.memory_repository import MemoryRepository, populate
import games.adapters.repository as repo
import games.utilities.services as services
import games.games_list._services as allGamesServices
import games.user_profile.services as user_profile_services
import games.gamedesc.services as gamedesc_services
from games.gamedesc.services import NonExistentGameException, UnknownUserException


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

# games_list tests:

def test_query_all_games_by_name():
    repo.repo_instance = MemoryRepository()
    allGames0 = allGamesServices.query_all_games_by_name(repo.repo_instance)
    assert allGames0 == []  # check list begins empty before populate is called
    populate(repo.repo_instance)
    allGames1 = allGamesServices.query_all_games_by_name(repo.repo_instance)
    assert allGames1 != []  # check populate works
    for i in range(len(allGames1) - 1):
        assert allGames1[i].title < allGames1[i+1].title  # check all games are in order by title


def test_query_games_title():
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)
    allGames = allGamesServices.query_all_games_by_name(repo.repo_instance)
    searched_games0 = allGamesServices.query_games_title("The", repo.repo_instance)
    assert searched_games0 != []  # checks that it returns items to the list
    for game in searched_games0:
        assert "the" in game.title.lower()  # checks that all items actually contain "the"
    searched_games1 = allGamesServices.query_games_title("", repo.repo_instance)
    assert len(searched_games1) == len(allGames)  # defaults to all games



def test_query_publisher():
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)
    allGames = allGamesServices.query_all_games_by_name(repo.repo_instance)
    searched_publishers0 = allGamesServices.query_publisher("a", repo.repo_instance)
    assert searched_publishers0 != []  # checks that it returns items to the list
    for game in searched_publishers0:
        assert "a" in game.publisher.publisher_name.lower()  # checks that all items actually contain "a"
    searched_publishers1 = allGamesServices.query_publisher("", repo.repo_instance)
    assert len(searched_publishers1) == len(allGames)  # defaults to all games


def test_query_genres():
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)
    search_term = "Adventure"
    allGames = allGamesServices.query_all_games_by_name(repo.repo_instance)
    searched_genres0 = allGamesServices.query_genre(search_term, repo.repo_instance)
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
    searched_genres1 = allGamesServices.query_genre("", repo.repo_instance)
    assert len(searched_genres1) == len(allGames)  # defaults to all games


# gamedesc Review tests:

def test_get_game():
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)
    game = gamedesc_services.get_game(7940, repo.repo_instance)
    assert "Call of Duty" in game.title

    with pytest.raises(NonExistentGameException):
        gamedesc_services.get_game(123454321, repo.repo_instance)

def test_add_review():
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)
    test_user = User('james', 'Password123')
    repo.repo_instance.add_user(test_user)
    test_game = repo.repo_instance.get_game(7940)

    with pytest.raises(NonExistentGameException):
        gamedesc_services.add_review('james', 123454321, 3, 'Good game', repo.repo_instance)

    with pytest.raises(UnknownUserException):
        gamedesc_services.add_review('lames', 7940, 3, 'Good game', repo.repo_instance)

    gamedesc_services.add_review('james', 7940, 3, 'Good game', repo.repo_instance)
    test_review1 = Review(test_user, test_game, 3, 'Good game')
    test_reviews = repo.repo_instance.get_reviews()

    assert test_review1 in test_reviews
    assert len(test_reviews) == 1

    gamedesc_services.add_review('james', 7940, 1, 'Bad game', repo.repo_instance)
    test_review2 = Review(test_user, test_game, 1, 'Bad game')
    test_reviews = repo.repo_instance.get_reviews()

    assert test_review1 not in test_reviews
    assert test_review2 in test_reviews
    assert len(test_reviews) == 1


def test_get_existing_review():
    pass


# user_profiile tests:
def test_profile_get_user():
    pass






