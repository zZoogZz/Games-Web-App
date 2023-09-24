import pytest

import games.adapters.repository as repo
import games.games_list._services as allGamesServices
import games.utilities.services as services
from games.adapters import memory_repository
from games.adapters.memory_repository import MemoryRepository, populate
from games.authentication.services import add_user, authenticate_user, get_user, user_to_dict
from games.domainmodel.model import Genre, User, Game, Review
from tests.conftest import in_memory_repo
import games.gamedesc.services as gamedesc_services
import games.user_profile.services as user_profile_services
from games.authentication.services import UnknownUserException
from games.gamedesc.services import NonExistentGameException



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


TESTUSERNAME = "USERNAME"
TESTPASSWORD = "PASSWORD"


class TestAuth:
    def test_authenticate_user(self):
        repo = memory_repository.MemoryRepository()

        add_user(TESTUSERNAME, TESTPASSWORD, repo)

        assert User(TESTUSERNAME, TESTPASSWORD) in repo.get_users()

    def test_duplicate_user(self):
        repo = memory_repository.MemoryRepository()

        add_user(TESTUSERNAME, TESTPASSWORD, repo)

        with pytest.raises(Exception):
            add_user(TESTUSERNAME, TESTPASSWORD, repo)

    def test_get_user(self):
        repo = memory_repository.MemoryRepository()

        add_user(TESTUSERNAME, TESTPASSWORD, repo)

        assert get_user(TESTUSERNAME, repo)['user_name'] == TESTUSERNAME.lower()
        assert str(repo.get_user(TESTUSERNAME)) == str(User(TESTUSERNAME, TESTPASSWORD))

    def test_get_users(self):
        repo = memory_repository.MemoryRepository()

        add_user(TESTUSERNAME, TESTPASSWORD, repo)

        assert str(repo.get_users()[0]) == str(User(TESTUSERNAME, TESTPASSWORD))

    def test_user_to_dict(self):
        test_user = User(TESTUSERNAME, TESTPASSWORD)
        user_dict = user_to_dict(test_user)

        assert test_user.username == user_dict['user_name']

# gamedesc Review tests:

def test_get_game():
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance, "./games/adapters/data/")
    game = gamedesc_services.get_game(7940, repo.repo_instance)
    assert "Call of Duty" in game.title

    with pytest.raises(NonExistentGameException):
        gamedesc_services.get_game(123454321, repo.repo_instance)

def test_add_review():
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance, "./games/adapters/data/")
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
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance, "./games/adapters/data/")
    test_user = User('james', 'Password123')
    repo.repo_instance.add_user(test_user)
    test_game1 = repo.repo_instance.get_game(7940)
    test_game2 = repo.repo_instance.get_game(1228870)

    #assert gamedesc_services.get_existing_review(test_game1, 'mystery_person') is None
    assert gamedesc_services.get_existing_review(test_game1, 'james') is None

    gamedesc_services.add_review('james', 7940, 3, 'Good game', repo.repo_instance)
    test_review1 = Review(test_user, test_game1, 3, 'Good game')

    assert gamedesc_services.get_existing_review(test_game1, 'james') == test_review1
    assert gamedesc_services.get_existing_review(test_game2, 'james') is None


# user_profiile tests:
def test_profile_get_user():
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance, "./games/adapters/data/")
    test_user = User('james', 'Password123')
    repo.repo_instance.add_user(test_user)

    #assert user_profile_services.get_user('mystery_person') is None
    assert user_profile_services.get_user('james') == test_user



class TestFavourite:
    def test_toggle_favourites(self):
        repo = memory_repository.MemoryRepository()
        test_user = User(TESTUSERNAME, TESTPASSWORD)
        test_game1 = Game(1, "Test")
        test_game2 = Game(2, "Test")

        repo.toggle_favourite(test_game1, test_user)

        assert repo.game_is_favourite(test_game1, test_user)
        assert not repo.game_is_favourite(test_game2, test_user)

        repo.toggle_favourite(test_game1, test_user)
        repo.toggle_favourite(test_game2, test_user)

        assert repo.game_is_favourite(test_game2, test_user)
        assert not repo.game_is_favourite(test_game1, test_user)

    def test_get_favourites(self):
        repo = memory_repository.MemoryRepository()
        test_user = User(TESTUSERNAME, TESTPASSWORD)
        test_game1 = Game(1, "Test")
        test_game2 = Game(2, "Test")

        repo.toggle_favourite(test_game1, test_user)
        repo.toggle_favourite(test_game2, test_user)

        assert str(repo.get_favourites(test_user)) == "[<Game 1, Test>, <Game 2, Test>]"

        repo.toggle_favourite(test_game1, test_user)

        assert str(repo.get_favourites(test_user)) == "[<Game 2, Test>]"