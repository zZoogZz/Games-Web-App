import pytest

from games.domainmodel.model import Game
from games.games_list._public_services import toggle_favourite
from games.games_list._services import query_all_games_by_name, query_games_title, query_publisher, query_genre, query_favourite_games, query_wishlist_games
import games.adapters.repository as repo
from games.adapters.memory_repository import MemoryRepository, populate
from games.authentication.services import add_user, authenticate_user
from flask import session




class TestTypes:
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)



    def test_query_all(self):
        assert type(query_all_games_by_name(repo)) == list

        with pytest.raises(AttributeError):
            query_all_games_by_name("TEST")

    def test_query_title(self):
        assert type(query_games_title("TEST",repo)) == list

        with pytest.raises(AttributeError):
            query_games_title(0)

    def test_query_publisher(self):
        assert type(query_publisher("TEST",repo)) == list

        with pytest.raises(AttributeError):
            query_publisher(0)

    def test_query_genre(self):
        assert type(query_genre("TEST",repo)) == list

        with pytest.raises(AttributeError):
            query_genre(0)

    def test_query_favourite_games(self, client):
        with client:
            TESTUSERNAME = "testuserdjdjdj"
            TESTPASSWORD = "testpassword123"
            add_user(TESTUSERNAME, TESTPASSWORD, repo.repo_instance)
            # set a user id without going through the login route
            response = client.post("/authentication/login", data={"user_name": TESTUSERNAME, "password": TESTPASSWORD})
            assert session['user_name'] == TESTUSERNAME
            assert response.status_code == 302
            assert "User name not recognised - please supply another" not in response.response

