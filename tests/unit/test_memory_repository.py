import pytest
import os
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.memory_repository import MemoryRepository, populate
from games.adapters.datareader.csvdatareader import GameFileCSVReader


# Functions to facilitate tests:

def create_csv_reader():
    dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    games_file_name = os.path.join(dir_name, "games/adapters/data/games.csv")
    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()
    return reader

# Actual tests:


def test_empty_repo():
    repo = MemoryRepository()
    assert repo.get_number_of_games() == 0
    assert repo.get_game(7940) == None
    assert repo.get_game_ids() == []
    assert repo.get_genres() == []
    with pytest.raises(KeyError):
        games_list0 = repo.get_game_ids_by_genre(Genre("Indie"))


def test_memory_repository():
    repo = MemoryRepository()
    reader = create_csv_reader()
    list_iterator = iter(reader.dataset_of_games)
    game1 = next(list_iterator)
    game2 = next(list_iterator)

    # Test repository adds games correctly
    repo.add_game(123456)
    repo.add_game("Not a game")
    assert repo.get_number_of_games() == 0
    repo.add_game(game1)
    assert repo.get_number_of_games() == 1
    repo.add_game(game1)
    assert repo.get_number_of_games() == 1
    assert repo.get_game_ids() == [7940]
    assert repo.get_genres() == [Genre("Action")]
    repo.add_game(game2)
    assert repo.get_number_of_games() == 2

    # Test repository can retrieve a game object:
    assert repo.get_game(123456) == None
    assert repo.get_game("Not a game") ==None
    assert repo.get_game(7940) == Game(game_id=7940, game_title="Call of Duty® 4: Modern Warfare®")

    populate(repo, "./games/adapters/data/")

    # Test repository retrieves correct number of game objects:
    assert repo.get_number_of_games() == 877

    # Test the number of unique genres in the dataset:
    assert len(repo.get_genres()) == 24
    repo.add_genre(Genre("New Genre"))

    # Test return all games as dictionary
    games = repo.get_games()
    assert len(games.keys()) == 877
    assert type(games[7940]) == Game

    # Test retrieving game ids
    assert len(repo.get_game_ids()) == 877
    assert type(repo.get_game_ids()[0]) == int

    # Test repository adds a new genre, and the count of genres increases by 1:
    assert len(repo.get_genres()) == 25
    repo.add_genre(Genre("New Genre"))
    assert len(repo.get_genres()) == 25

    # Test game id retrieval by genre
    assert repo.get_game_ids_by_genre(Genre("Indie"))[:3] == [299380, 448500, 1297010]
    with pytest.raises(KeyError):
        games_list0 = repo.get_game_ids_by_genre(Genre("Fake Genre"))
    with pytest.raises(KeyError):
        games_list0 = repo.get_game_ids_by_genre(Genre(123456))

    # Test retrieval per release date
    assert repo.get_game_ids_on_date("Apr 24, 2021") == [1576880, 1580990]
    assert repo.get_game_ids_on_date("Apr 3, 1234") == []
    assert repo.get_game_ids_on_date(123456) == []

    assert repo.get_previous_release_date("Apr 26, 2021") == ("Apr 24, 2021")
    assert repo.get_previous_release_date("Apr 26, 1723") is None
    first_date = last_date = repo.get_sorted_release_dates()[0].strftime("%b %d, %Y")
    assert repo.get_previous_release_date(first_date) is None
    with pytest.raises(ValueError):
        previous_date = repo.get_previous_release_date("An invalid string")
    with pytest.raises(TypeError):
        next_date = repo.get_previous_release_date(1234567)

    assert repo.get_next_release_date("Apr 24, 2021") == ("Apr 26, 2021")
    assert repo.get_next_release_date("Apr 26, 1723") is None
    last_date = repo.get_sorted_release_dates()[-1].strftime("%b %d, %Y")
    assert repo.get_next_release_date(last_date) is None
    with pytest.raises(ValueError):
        next_date = repo.get_next_release_date("An invalid string")
    with pytest.raises(TypeError):
        next_date = repo.get_next_release_date(123456)

    # Test retrieval of game id list sorted by title
    assert repo.get_game_ids_sorted_by_title()[:3] == [435790, 1684530, 796580]

    # Test retrieval by game id list
    assert repo.get_games_by_ids([1588070, 1939600]) == [Game(game_id=1588070, game_title="DuckMan"),
                                                         Game(game_id=1939600, game_title="Sillage")]
    assert repo.get_games_by_ids(["not an id", 99999999999]) == []

    # Test retrieval by publisher
    assert repo.get_game_ids_by_publisher(Publisher("Arcen Games, LLC")) == [471770, 40420]
    assert repo.get_game_ids_by_publisher(Publisher("Not a real Publisher")) == []
    assert repo.get_game_ids_by_publisher(123456) == []



