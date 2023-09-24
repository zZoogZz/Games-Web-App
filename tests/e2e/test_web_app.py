import pytest
from games.authentication.services import add_user
from flask import session
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


