import pytest
from games import create_app
from games.adapters import memory_repository
from utils import get_project_root

TEST_DATA_PATH = get_project_root() / "tests" / "data"


@pytest.fixture
def in_memory_repo():
    repo = memory_repository.MemoryRepository()
    database_mode = False
    memory_repository.populate(repo, TEST_DATA_PATH)
    return repo


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'REPOSITORY': 'memory',
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False
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
