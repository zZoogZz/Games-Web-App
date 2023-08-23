import pytest
import os
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.memory_repository import MemoryRepository, populate
from games.adapters.datareader.csvdatareader import GameFileCSVReader


# Functions to facilitate tests:
def initialise_repo():
    repo = MemoryRepository()
    populate(repo)
    return repo


def create_csv_reader():
    dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    games_file_name = os.path.join(dir_name, "games/adapters/data/games.csv")
    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()
    return reader


def test_add_and_get_games():
    repo = MemoryRepository()
    reader = create_csv_reader()
    game = next(iter(reader.dataset_of_games))

    # Test repository can add a game object
    repo.add_game(game)
    assert repo.get_number_of_games() == 1
    assert repo.get_game_ids() == [7940]
    assert repo.get_genres() == [Genre("Action")]

    # Test repository can retrieve a game object:
    assert repo.get_game(7940) == Game(game_id=7940, game_title="Call of Duty® 4: Modern Warfare®")

    repo.add_game(game)
    assert repo.get_number_of_games() == 1

    populate(repo)

    # Test repository retrieves correct number of game objects:
    assert repo.get_number_of_games() == 877

    # Test the number of unique genres in the dataset:
    assert len(repo.get_genres()) == 24
    repo.add_genre(Genre("New Genre"))

    # Test repository adds a new genre, and the count of genres increases by 1:
    assert len(repo.get_genres()) == 25
    repo.add_genre(Genre("New Genre"))
    assert len(repo.get_genres()) == 25

    assert repo.get_game_ids_by_genre(Genre("Indie"))[:3] == [299380, 448500, 1297010]
    assert repo.get_game_ids_on_date("Apr 24, 2021") == [1576880, 1580990]
    assert repo.get_game_ids_sorted_by_title()[:3] == [435790, 1684530, 796580]
    assert repo.get_games_by_ids([1588070, 1939600]) == [Game(game_id=1588070, game_title="DuckMan"),
                                                         Game(game_id=1939600, game_title="Sillage")]

    assert repo.get_game_ids_by_publisher(Publisher("Arcen Games, LLC")) == [471770, 40420]

    # Test repository search games by title or publisher etc
    matching_ids = []
    search_term = "shape"
    for game_id in repo.get_game_ids_sorted_by_title():
        if search_term.lower() in repo.get_game(game_id).title.lower():
            matching_ids.append(game_id)
    assert matching_ids == [1375270, 1143900]


