from datetime import date, datetime

import pytest

import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import Publisher, Genre, Game, Review, User
from games.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    """
    Creates two users and tests that users are added correctly to the database.
    """
    test_repo = SqlAlchemyRepository(session_factory)
    user = User('Dave', '123456789')
    test_repo.add_user(user)
    user2 = User('Martin', '123456789')
    test_repo.add_user(user2)
    retrieved_user = test_repo.get_user('dave')
    assert retrieved_user == user and retrieved_user is user


def test_repository_can_retrieve_a_user(session_factory):
    """
    Adds a user to the database and then tests that it can be retrieved.
    """
    test_repo = SqlAlchemyRepository(session_factory)
    user = User('User1', '8734gfe2058v')
    test_repo.add_user(user)
    retrieved_user = test_repo.get_user('user1')
    assert retrieved_user == User('User1', '8734gfe2058v') and retrieved_user is user


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    """
    Tests that a non-existent user can NOT be retrieved.
    """
    test_repo = SqlAlchemyRepository(session_factory)
    user = test_repo.get_user('non-existent-user')
    assert user is None


def test_repository_can_add_a_game(session_factory):
    """
    Creates two games and tests that games are added correctly to the database.
    """
    test_repo = SqlAlchemyRepository(session_factory)
    game = Game(123, 'Hearts')
    game.price = 69
    game.release_date = 'Oct 21, 2008'
    test_repo.add_game(game)
    retrieved_game = test_repo.get_game(123)
    assert retrieved_game == game


def test_repository_can_retrieve_a_game(session_factory):
    """
    Adds a game to the database and then tests that it can be retrieved.
    """
    test_repo = SqlAlchemyRepository(session_factory)
    game = Game(123, 'Game1')
    game.price = 69
    game.release_date = 'Oct 21, 2008'
    test_repo.add_game(game)
    retrieved_game = test_repo.get_game(123)
    assert retrieved_game == game


def test_repository_does_not_retrieve_a_non_existent_game(session_factory):
    """
    Tests that a non-existent game can NOT be retrieved.
    """
    test_repo = SqlAlchemyRepository(session_factory)
    retrieved_game = test_repo.get_game(69)
    assert retrieved_game is None


def test_repository_can_get_all_games(session_factory):
    """
    Tests that the database populates the expected number of games.
    Also checks that get_games() function operates correctly.
    """
    test_repo = SqlAlchemyRepository(session_factory)
    all_games = test_repo.get_games()
    assert len(all_games) == 877


def test_repository_can_get_games_by_game_ids(session_factory):
    """
    Checks that games can be retrieved by their game IDs
    """
    test_repo = SqlAlchemyRepository(session_factory)
    all_game_ids = test_repo.get_game_ids()
    assert len(all_game_ids) == 877
    all_games = test_repo.get_games_by_ids(all_game_ids)
    assert len(all_games) == 877


def test_repository_user_can_add_a_review(session_factory):
    """
    Checks that a user can add a review to a game.
    """
    test_repo = SqlAlchemyRepository(session_factory)
    # Initialise
    user = User('User', 'Password!123')
    test_repo.add_user(user)
    game = Game(1, "Test Game")
    game.price = 69
    game.release_date = 'Oct 21, 2008'
    test_repo.add_game(game)

    # Get Objects from Database
    retrieved_game = test_repo.get_game(1)
    retrieved_user = test_repo.get_user('user')

    # Add a review, check the review was added.
    review = Review(retrieved_user, retrieved_game, 5, "Great game!")
    test_repo.add_review(review)
    assert review in test_repo.get_reviews()


def test_repository_favorite_testing(session_factory):
    """
    Tests that a game can be added and removed from a users favourite. Using the toggle.
    """
    test_repo = SqlAlchemyRepository(session_factory)

    # Create User
    user = User('User', 'Password!123')
    test_repo.add_user(user)

    # Create Game
    game = Game(430, 'Hearts')
    game.price = 69
    game.release_date = 'Oct 21, 2008'
    test_repo.add_game(game)

    # Get User & Game
    retrieved_user = test_repo.get_user('user')
    retrieved_game = test_repo.get_game(430)

    # Check the user does not have any favourites before any are set.
    assert test_repo.get_favourites(retrieved_user) == []

    # Add and Check the above game is in the favourites list by toggling it.
    test_repo.toggle_favourite(retrieved_game, retrieved_user)
    assert retrieved_game in test_repo.get_favourites(retrieved_user)

    # Check toggling again removes the game from the list.
    test_repo.toggle_favourite(retrieved_game, retrieved_user)
    assert test_repo.get_favourites(retrieved_user) == []

