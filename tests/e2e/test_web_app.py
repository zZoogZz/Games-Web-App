import pytest
from games.authentication.services import add_user
from flask import session

from games.domainmodel.model import Game
from games.games_list._public_services import is_favourite, get_favourites
from tests.conftest import client, app, runner
from games.adapters.memory_repository import MemoryRepository, populate
import games.adapters.repository as repo

TESTUSERNAME = "testuserdjdjdj"
TESTPASSWORD = "testpassword123"


class TestAuth:

    def test_successful_login(self, client):
        """
        Correct user and password, expect login action.
        """
        with client:
            add_user(TESTUSERNAME, TESTPASSWORD, repo.repo_instance)
            # set a user id without going through the login route

            response = client.post("/authentication/login", data={"user_name": TESTUSERNAME, "password": TESTPASSWORD})
            assert session['user_name'] == TESTUSERNAME
            assert response.status_code == 302
            html = response.data.decode('utf-8')
            assert "User name not recognised - please supply another" not in html
            assert "Password does not match supplied user name - please check and try again" not in html

    def test_incorrect_password_login(self, client):
        with client:
            add_user(TESTUSERNAME, TESTPASSWORD, repo.repo_instance)
            # set a user id without going through the login route

            response = client.post("/authentication/login", data={"user_name": TESTUSERNAME, "password": "INCORRECTPASSWORD"})
            with pytest.raises(KeyError):
                session['user_name']
            assert response.status_code == 200
            html = response.data.decode('utf-8')
            assert "User name not recognised - please supply another" not in html
            assert "Password does not match supplied user name - please check and try again" in html

    def test_incorrect_username_login(self, client):
        with client:
            # add_user(TESTUSERNAME, TESTPASSWORD, repo.repo_instance)
            # set a user id without going through the login route

            response = client.post("/authentication/login", data={"user_name": TESTUSERNAME, "password": TESTPASSWORD})
            with pytest.raises(KeyError):
                session['user_name']
            assert response.status_code == 200
            html = response.data.decode('utf-8')
            assert "User name not recognised - please supply another" in html
            assert "Password does not match supplied user name - please check and try again" not in html

    def test_logout(self, client):
        with client:
            add_user(TESTUSERNAME, TESTPASSWORD, repo.repo_instance)
            client.post("/authentication/login", data={"user_name": TESTUSERNAME, "password": TESTPASSWORD})

            assert session['user_name'] == TESTUSERNAME

            response = client.get("/authentication/logout")

            with pytest.raises(KeyError):
                session['user_name']

            assert response.status_code == 302


class TestPagesUnauthenticated:
    def test_home_page(self, client):
        with client:
            response = client.get('/')
            assert response.status_code == 200
            assert "Welcome to our CS235 game library webapp." in response.data.decode('utf-8')

    def test_all_games_page(self, client):
        with client:
            response = client.get('/games/all')
            assert response.status_code == 200
            assert "All Games" in response.data.decode('utf-8')

    def test_game_desc_page(self, client):
        # TODO Manually control this test data.
        with client:
            response = client.get('/game/435790')
            assert response.status_code == 200
            assert "10 Second Ninja X" in response.data.decode('utf-8')

    def test_review(self, client):
        # TODO Manually control this test data.
        with client:
            response = client.get('/review?game=435790&sort_choice=Highest+Rating')
            assert response.status_code == 302

    def test_favourite_toggle(self, client):
        with client:
            response = client.post('/game/435790', data={"toggle_favourite": True})
            assert response.status_code == 302
            assert "login" in response.data.decode("utf-8")

    def test_profile_page(self, client):
        with client:
            response = client.get('/user_profile/')
            assert response.status_code == 302
            assert "login" in response.data.decode("utf-8")

    def test_favourites_page(self, client):
        with client:
            response = client.get('/games/list/favourites/')
            # assert response.status_code == 302 TODO: Re-enable this check.
            assert "login" in response.data.decode("utf-8" )


@pytest.fixture()
def login(client):
    with client:
        add_user(TESTUSERNAME, TESTPASSWORD, repo.repo_instance)
        client.post("/authentication/login", data={"user_name": TESTUSERNAME, "password": TESTPASSWORD})


class TestPagesAuthenticated:
    def test_favourite_toggle(self, client, login):
        with client:
            first_response = client.get('/game/435790')
            assert session['user_name'] == TESTUSERNAME

            assert first_response.status_code == 200
            assert "Favourite" in first_response.data.decode('utf-8')

            second_response = client.post('/game/435790', data={'action':'toggle_favourite'})
            assert second_response.status_code == 302
            assert is_favourite(Game(435790,"Test"), repo)

            third_response = client.get('/game/435790')
            assert third_response.status_code == 200
            assert "Unfavourite" in third_response.data.decode('utf-8')


