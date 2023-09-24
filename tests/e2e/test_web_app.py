import pytest
from flask import session
# from games.games_list._public_services import toggle_favourite
# import games.adapters.repository as repo


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
		('test', 'Abcdef1', b'Your password must be at least 8 characters, and contain an upper case letter, a lower case letter and a digit'),
		('test', 'abcdef12', b'Your password must be at least 8 characters, and contain an upper case letter, a lower case letter and a digit'),
		('test', 'Abcdefgh', b'Your password must be at least 8 characters, and contain an upper case letter, a lower case letter and a digit'),
		('test', 'ABCDEF12', b'Your password must be at least 8 characters, and contain an upper case letter, a lower case letter and a digit'),
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



	"""
	#Can't get the following to work, some issue with using toggle_favourites here
	
	from games.games_list._public_services import toggle_favourite
	import games.adapters.repository as repo
	
	for game_id in [7940, 1228870, 311120, 410320, 418650]:
		game = repo.repo_instance.get_game(game_id)
		toggle_favourite(game, repo.repo_instance)

	response = client.get('/user_profile/')
	assert b'You have not added any favourites.' not in response.data
	assert b'<div class="favourites-list"><a href="/game/7940">' in response.data
	
	"""


