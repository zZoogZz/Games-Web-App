from datetime import date, datetime

import pytest

import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    #Creates test_repo and then creates two users and tests that users are added correctly.
    test_repo = SqlAlchemyRepository(session_factory)
    user = User('Dave', '123456789')
    test_repo.add_user(user)
    user2 = User('Martin', '123456789')
    test_repo.add_user(user2)
    retrieved_user = test_repo.get_user('Dave')
    assert retrieved_user == user and retrieved_user is user

