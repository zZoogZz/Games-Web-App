import os
from pathlib import Path

from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.repository import AbstractRepository


def populate(repo: AbstractRepository, data_path: Path, repository_type):
    games_file_name = os.path.join(data_path, "games.csv")
    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()
    games = reader.dataset_of_games

    if repository_type == 'memory':
        for game in games:
            repo.add_game(game)

    elif repository_type == 'database':
        for game in games:
            repo.add_game(game)

    else:
        raise ValueError("Repository Type not specified correctly at population.")

