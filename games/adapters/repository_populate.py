import os
from pathlib import Path

from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.repository import AbstractRepository


def populate(repo, data_path, repository_type):
    games_file_name = os.path.join(data_path, "games.csv")
    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()
    publishers = reader.dataset_of_publishers
    genres = reader.dataset_of_genres
    games = reader.dataset_of_games


    if repository_type == 'memory':
        print("Memory Type")
        for game in games:
            repo.add_game(game)

    elif repository_type == 'database':
        for genre in genres:
            repo.add_genre(genre)

        for publisher in publishers:
            repo.add_publisher(publisher)

        for game in games:
            repo.add_game(game)


    else:
        raise ValueError("Repository Type not specified correctly at population.")

