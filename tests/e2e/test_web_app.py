import pytest

from games.authentication.services import add_user
from flask import session
from games.domainmodel.model import Game, Review
from games.games_list._public_services import is_favourite, get_favourites
from tests.conftest import client, app, runner
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

			response = client.post("/authentication/login",
								   data={"user_name": TESTUSERNAME, "password": "INCORRECTPASSWORD"})
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
			response = client.get('/game/7940')
			assert response.status_code == 200
			assert "Call of Duty" in response.data.decode('utf-8')

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
			assert "login" in response.data.decode("utf-8")


@pytest.fixture()
def login(client):
	with client:
		add_user(TESTUSERNAME, TESTPASSWORD, repo.repo_instance)
		client.post("/authentication/login", data={"user_name": TESTUSERNAME, "password": TESTPASSWORD})


class TestPagesAuthenticated:
	def test_favourite_toggle(self, client, login):
		with client:
			first_response = client.get('/game/7940')
			assert session['user_name'] == TESTUSERNAME

			assert first_response.status_code == 200
			assert "Favourite" in first_response.data.decode('utf-8')

			second_response = client.post('/game/7940', data={'action': 'toggle_favourite'})
			assert second_response.status_code == 302
			assert is_favourite(Game(7940, "Test"), repo)

			third_response = client.get('/game/7940')
			assert third_response.status_code == 200
			assert "Unfavourite" in third_response.data.decode('utf-8')

	def test_profile_page(self, client, login):
		with client:
			response = client.get('/user_profile/')
			assert response.status_code == 200
			assert session['user_name'] == TESTUSERNAME
			assert "{}'s Profile".format(TESTUSERNAME) in response.data.decode('utf-8')


def test_register(client, auth):
	# Check that we retrieve the register page.
	response_code = client.get('/authentication/register').status_code
	assert response_code == 200

	# Check that we can register a user successfully, supplying a valid user name and password.
	response = client.post(
		'/authentication/register',
		data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
	)
	assert response.headers['Location'] == '/authentication/login'

	# Check auth.register() also works:
	response = auth.register()
	assert response.status_code == 302
	assert response.headers['Location'] == '/authentication/login'


def test_login(client, auth):
	# Check login page status
	status_code = client.get('/authentication/login').status_code
	assert status_code == 200

	# Register 'spork' user
	auth.register()

	response = auth.login()
	# Check login successful and redirects to home
	assert response.status_code == 302
	assert response.headers['Location'] == '/'

	# Check that a session has been created for the logged-in user.
	with client:
		client.get('/')
		assert session['user_name'] == 'spork'


def test_logout(client, auth):
	auth.login()
	with client:
		# Check that logging out clears the user's session.
		auth.logout()
		assert 'user_id' not in session


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
		('', 'Abcdef12', b'Your user name is required'),
		('a', 'Abcdef12', b'Your user name is too short'),
		('test', '', b'Your password is required'),
		('test', 'Abcdef1',
		 b'Your password must be at least 8 characters, and contain an upper case letter, a lower case letter and a digit'),
		('test', 'abcdef12',
		 b'Your password must be at least 8 characters, and contain an upper case letter, a lower case letter and a digit'),
		('test', 'Abcdefgh',
		 b'Your password must be at least 8 characters, and contain an upper case letter, a lower case letter and a digit'),
		('test', 'ABCDEF12',
		 b'Your password must be at least 8 characters, and contain an upper case letter, a lower case letter and a digit'),
		('spork', 'Abcdef12', b'Your user name is already taken - please supply another'),
))
def test_registration_bad_input(client, user_name, password, message, auth):
	# Check that attempting to register with invalid combinations of user name and password generate appropriate error
	# messages.
	auth.register(user_name='spork', password='Password123')
	response = client.post(
		'/authentication/register',
		data={'user_name': user_name, 'password': password}
	)
	print(response.data)
	assert message in response.data


def test_reviews(client, auth):
	# Check redirect when no user logged in
	response = client.get('/review?game=7940&sort_choice=Highest+Rating')
	assert response.status_code == 302  # Check redirect status
	assert response.headers['Location'] == '/authentication/login'

	auth.register()
	auth.login()

	# Check review page opens when logged in
	response = client.get('/review?game=7940&sort_choice=Highest+Rating')
	assert response.status_code == 200

	# Post first review
	response = client.post('/review', data={'review': 'First review.', 'rating': 3, 'game_id': 7940})

	# Check submitting review redirects to game description and review content is present
	assert response.status_code == 302  # Check redirect status
	assert response.headers['Location'] == '/game/7940?sort_choice=Highest+Rating'
	response = client.get(response.headers['Location'])
	assert b'First review.' in response.data

	# Check submitting another review from same user overwrites old review.
	response = client.post('/review', data={'review': 'Second review.', 'rating': 3, 'game_id': 7940})
	assert response.status_code == 302  # Check redirect status
	assert response.headers['Location'] == '/game/7940?sort_choice=Highest+Rating'
	response = client.get(response.headers['Location'])
	assert b'First review.' not in response.data
	assert b'Second review.' in response.data


def test_user_links(client, auth):
	# Check user profile links appropriate when not logged in
	response = client.get('/')
	assert b'<a href="/authentication/login">Login</a>' in response.data
	assert b'<a href="/authentication/register">Register</a>' in response.data
	assert b'You are logged in' not in response.data
	assert b'<a href="/user_profile/">' not in response.data
	assert b'<a href="/authentication/logout">Logout</a>' not in response.data

	auth.register()
	auth.login()

	# Check user profile links appropriate when not logged in
	response = client.get('/')
	assert b'<a href="/authentication/login">Login</a>' not in response.data
	assert b'<a href="/authentication/register">Register</a>' not in response.data
	assert b'You are logged in as spork' in response.data
	assert b'<a href="/user_profile/">' in response.data
	assert b'<a href="/authentication/logout">Logout</a>' in response.data


def test_profile_page(client, auth):
	# Check user profile redirects to login page
	response = client.get('/user_profile/')
	assert response.status_code == 302  # Check redirect status
	assert response.headers['Location'] == '/authentication/login'

	auth.register()
	auth.login()

	response = client.get('/user_profile/')
	assert response.status_code == 200  # Check redirect status
	assert b'spork\'s Profile' in response.data
	assert b'You have not added any favourites.' in response.data
	assert b'You have not reviewed any games.' in response.data

	# Add games into favourites to test profile page handling.
	with client:
		client.get('/')
		user = repo.repo_instance.get_user(session['user_name'])

	test_game_ids = [7940, 1228870, 311120, 410320, 418650]
	for game_id in test_game_ids:
		game = repo.repo_instance.get_game(game_id)
		user.add_favourite_game(game)

	response = client.get('/user_profile/')
	assert b'You have not added any favourites.' not in response.data
	assert b'<div class="favourites-list"><a href="/game/7940">' in response.data
	assert b'<div class="favourites-list"><a href="/game/1228870">' in response.data
	assert b'<div class="favourites-list"><a href="/game/311120">' in response.data
	assert b'<div class="favourites-list"><a href="/game/410320">' in response.data
	assert b'<div class="favourites-list"><a href="/game/418650">' in response.data

	# Add reviews to user to test profile page handling.
	test_game_reviews = [("Terrible", 1), ("Great", 5)]
	with client:
		client.get('/')
		user = repo.repo_instance.get_user(session['user_name'])

	for i in range(len(test_game_reviews)):
		game = repo.repo_instance.get_game(test_game_ids[i])
		user.add_review(Review(user, game, test_game_reviews[i][1], test_game_reviews[i][0]))

	response = client.get('/user_profile/')
	assert b'You have not reviewed any games.' not in response.data
	assert b'Terrible' in response.data
	assert b'Great' in response.data
	assert (b'<img src="/static/gold_star.png" width="15" height="15">'
	        b'<img src="/static/grey_star.png" width="15" height="15">') in response.data

