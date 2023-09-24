import csv
import os.path
from pathlib import Path
from datetime import date, datetime
from typing import List

# from bisect import bisect, bisect_left, insort_left # using dict so no sorting by id required

# from werkzeug.security import generate_password_hash # no users or passwords yet

from games.adapters.repository import AbstractRepository, RepositoryException
from games.domainmodel.model import Game, Genre, Publisher, User, Review, Wishlist
from games.adapters.datareader.csvdatareader import GameFileCSVReader


class MemoryRepository(AbstractRepository):  # implement games ordered by date. id is assumed unique.

    def __init__(self):
        self.__games = dict()
        self.__genres = list()
        self.__games_by_genre = dict()
        self.__games_by_publisher = dict()
        self.__games_by_release_date = dict()
        self.__users = list()
        self.__reviews = list()

    def add_user(self, user: User):
        if isinstance(user, User):
            self.__users.append(user) # check

    def check_username_unique(self, username: str):
        for user in self.__users:
            if username.lower() == user.username.lower():
                return False
        return True


    def get_user(self, username: str) -> User:
        try:
            user = next((user for user in self.__users if user.username == username), None)  # check
            return user
        except ValueError:
            raise ValueError("username invalid or not found")

    def add_game(self, game: Game):
        if isinstance(game, Game) and game.game_id not in self.__games.keys():
            self.__games[game.game_id] = game
            self.add_game_id_to_release_date(game.game_id, game.release_date)
            for genre in game.genres:
                self.add_game_id_to_genre(game.game_id, genre)
                self.add_genre(genre)
            self.add_game_id_to_publisher(game.game_id, game.publisher)

    def get_game(self, game_id: int) -> Game:
        game = None
        try:
            game = self.__games[game_id]
        except KeyError:
            # No game fore this id
            return None
        return game

    def get_games(self):
        return self.__games

    def get_game_ids(self):
        print(self.__games.keys())
        return list(self.__games.keys())

    def add_game_id_to_genre(self, game_id: int, genre: Genre):
        if not isinstance(game_id, int) and not isinstance(genre, Genre):
            return
        if genre not in self.__games_by_genre.keys():
            self.__games_by_genre[genre] = [game_id]
        else:
            self.__games_by_genre[genre].append(game_id)

    def add_game_id_to_release_date(self, game_id: int, release_date: str):
        if release_date not in self.__games_by_release_date.keys():
            self.__games_by_release_date[release_date] = [game_id]
        else:
            self.__games_by_release_date[release_date].append(game_id)

    def add_game_id_to_publisher(self, game_id: int, publisher: Publisher):
        if publisher not in self.__games_by_publisher.keys():
            self.__games_by_publisher[publisher] = [game_id]
        else:
            self.__games_by_publisher[publisher].append(game_id)

    def get_game_ids_on_date(self, release_date: str) -> List[int]:
        try:
            return self.__games_by_release_date[release_date]
        except KeyError:
            # No games for specified date. Simply return an empty list.
            pass
        return []

    def get_number_of_games(self):
        return len(self.__games)

    def get_games_by_ids(self, game_id_list: List[int]) -> List[Game]:
        if not isinstance(game_id_list, List):
            return []
        else:
            for item in game_id_list:
                if not isinstance(item, int):
                    return []
        # Strip out any ids in id_list that don't represent game ids in the repository.
        game_ids = [game_id for game_id in game_id_list if game_id in self.__games.keys()]
        # Fetch the games.
        games = [self.__games[game_id] for game_id in game_ids]
        return games

    def get_game_ids_by_genre(self, genre: Genre):
        if not isinstance(genre, Genre):
            return []
        try:
            return self.__games_by_genre[genre]
        except ValueError:
            # Not found so return None
            pass
        return []

    def get_game_ids_sorted_by_title(self) -> List[int]:
        title_id_tuple_list = []
        for game in self.__games.values():
            title_id_tuple_list.append((game.title, game.game_id))
        title_id_tuple_list.sort()
        id_list = []
        for item in title_id_tuple_list:
            id_list.append(item[1])
        return id_list

    def get_sorted_release_dates(self):
        date_list = []
        for release_date in self.__games_by_release_date.keys():
            release_datetime = datetime.strptime(release_date, "%b %d, %Y")
            date_list.append(release_datetime)
        return sorted(date_list)

    # Not sure if get date of game required for us
    def get_previous_release_date(self, release_date: str):
        try:
            # Check if the release_date string is in the correct date format (e.g., "Oct 21, 2008")
            release_date = datetime.strptime(release_date, "%b %d, %Y")
        except ValueError:
            raise ValueError("Release date must be in 'Oct 21, 2008' format.")
        except TypeError:
            raise TypeError("Release date must be a string in 'Oct 21, 2008' format.")
        date_sequence = self.get_sorted_release_dates()
        if release_date in date_sequence:
            index = date_sequence.index(release_date) - 1
            if index not in range(len(date_sequence)):
                return None
            return date_sequence[index].strftime("%b %d, %Y")
        return None

    def get_next_release_date(self, release_date: str):
        try:
            # Check if the release_date string is in the correct date format (e.g., "Oct 21, 2008")
            release_date = datetime.strptime(release_date, "%b %d, %Y")
        except ValueError:
            raise ValueError("Release date must be in 'Oct 21, 2008' format.")
        except TypeError:
            raise TypeError("Release date must be a string in 'Oct 21, 2008' format.")
        date_sequence = self.get_sorted_release_dates()
        if release_date in date_sequence:
            index = date_sequence.index(release_date) + 1
            if index not in range(len(date_sequence)):
                return None
            return date_sequence[index].strftime("%b %d, %Y")
        return None

    def get_game_ids_by_publisher(self, publisher: Publisher) -> List[int]:
        try:
            return self.__games_by_publisher[publisher]
        except KeyError:
            # No games for specified publisher or publisher invalid. Return an empty list.
            pass
        return []

    def add_genre(self, genre: Genre):
        if not isinstance(genre, Genre):
            return
        if genre not in self.__genres:
            self.__genres.append(genre)

    def get_genres(self) -> List[Genre]:
        return self.__genres

    def add_review(self, review: Review):
        # call parent class first, add_review relies on implementation of code common to all derived classes
        super().add_review(review)
        self.__reviews.append(review)

    def remove_review(self, review: Review):

        if review in self.__reviews:
            # super().remove_review(review)
            self.__reviews.remove(review)
            print("remove attempted")
        else:
            print("failed to remove")

    def get_reviews(self):
        return self.__reviews

    # Helper method to return game index.
    # def game_index(self, game: Game):
    #     index = bisect_left(self.__games, game)
    #     if index != len(self.__games) and self.__games[index].release_date == game.release_date:
    #         return index
    #     raise ValueError


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read (effectively skip) first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def populate(repo: MemoryRepository, data_path):
    # Per lecture 12:
    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(data_path, "games.csv")
    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()
    games = reader.dataset_of_games
    for game in games:
        repo.add_game(game)


