import pytest
from flask import session


def test_register(client):
	# Check that we retrieve the register page.
	response_code = client.get('/authentication/register').status_code
	assert response_code == 200

	# Check that we can register a user successfully, supplying a valid user name and password.
	response = client.post(
		'/authentication/register',
		data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
	)
	assert response.headers['Location'] == '/authentication/login'


"""
@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data
"""


def test_login(client, auth):
	# Check that we can retrieve the login page.
	status_code = client.get('/authentication/login').status_code
	assert status_code == 200

	auth.register()

	response = client.post(
		'/authentication/login',
		data={'user_name': 'spork', 'password': 'Password123'}
	)
	print(response.headers['Location'])
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


"""
def test_reviews(client, auth):
	response = auth.login(user_name='thorke', password='cLQ^C#oFXloS')
	assert response.status_code == 200  # Assuming a successful login returns HTTP 200 OK
	#
	response = client.get('/review?game=7940&sort_choice=Highest+Rating')
	assert response.headers['Location'] == '/123?'

	response = client.post(
		'/review',
		data={'review': 'This is a great game.', 'rating': 3, 'game_id': 7940}
	)
	assert response.headers['Location'] == '/456?'

"""

"""
@pytest.mark.parametrize(('user_name', 'password', 'message'), (

)
"""
