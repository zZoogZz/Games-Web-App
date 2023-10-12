import pytest
from games import create_app
from games.adapters import memory_repository, repository_populate
from utils import get_project_root

SMALL_TEST_DATA_PATH = get_project_root() / "tests" / "data"
FULL_TEST_DATA_PATH = './games/adapters/data/'

@pytest.fixture
def in_memory_repo():
    repo = memory_repository.MemoryRepository()
    # database_mode = False
    repository_populate.populate(repo, TEST_DATA_PATH, 'memory')
    return repo


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'REPOSITORY': 'memory',
        'TEST_DATA_PATH': FULL_TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False,
    })
    # other setup can go here

    yield app


# clean up / reset resources here


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def register(self, user_name='spork', password='Password123'):
        return self.__client.post('authentication/register', data={'user_name': user_name, 'password': password})

    def login(self, user_name='spork', password='Password123'):
        return self.__client.post('authentication/login', data={'user_name': user_name, 'password': password})

    def logout(self):
        return self.__client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
