import csv
from pathlib import Path
from datetime import date, datetime
from typing import List

#from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from games.adapters.repository import AbstractRepository, RepositoryException
from games.domainmodel.model import Game, Genre, Publisher, User, Review, Wishlist


class MemoryRepository(AbstractRepository): # implement games ordered by date. id is assumed unique.

    def __init__(self):
        self.__games = dict()
        self.__genres = list()
        self.__games_by_genre = dict()
        self.__games_by_publisher = dict()
        self.__games_by_release_date = dict()
        self.__users = list()
        self.__reviews = list()

    def add_user(self, user: User):
        self.__users.append(user) # check

    def get_user(self, username) -> User:
        return next((user for user in self.__users if user.username == username), None) # check

    def add_game(self, game: Game):
        if isinstance(game, Game) and game.game_id not in self.__games.keys():
            self.__games[game.game_id] = game
            self.add_game_id_to_release_date(game.game_id, game.release_date)
            for genre in game.genres:
                self.add_game_id_to_genre(game.game_id, genre)
            self.add_game_id_to_publisher(game.game_id, game.publisher)

    def get_game(self, game_id: int) -> Game:
        game = None
        try:
            game = self.__games[game_id]
        except KeyError:
            pass  # Ignore exception and return None.
        return game

    def add_game_id_to_genre(self, game_id: int, genre: Genre):
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
        except ValueError:
            # No games for specified date. Simply return an empty list.
            pass
        return []

    def get_number_of_games(self):
        return len(self.__games)

    def get_first_game(self):
        if self.get_number_of_games() > 0:
            #not implemented yet
            game = self.__games[0]
        return None

    def get_last_game(self):
        if self.get_number_of_games() > 0:
            #not implemented yet
            game = self.__games[0]
        return None

    def get_games_by_ids(self, game_id_list):
        # Strip out any ids in id_list that don't represent game ids in the repository.
        game_ids = [game_id for game_id in game_id_list if game_id in self.__games.keys()]
        # Fetch the games.
        games = [self.__games[game_id] for game_id in game_ids]
        return games

    def get_game_ids_by_genre(self, genre: Genre):
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
    def get_date_of_previous_game(self, game: Game):
        date_sequence = self.get_sorted_release_dates()
        if game.release_date in date_sequence:
            try:
                index = date_sequence.index(game.release_date) - 1
                return date_sequence[index].strftime("%b %d, %Y")
            except ValueError:
                # No earlier games, so return None.
                pass
        return None

    def get_date_of_next_game(self, game: Game):
        date_sequence = self.get_sorted_release_dates()
        if game.release_date in date_sequence:
            try:
                index = date_sequence.index(game.release_date) + 1
                return date_sequence[index].strftime("%b %d, %Y")
            except ValueError:
                # No earlier games, so return None.
                pass
        return None

    def get_game_ids_by_publisher(self, publisher: Publisher) -> List[int]:
        try:
            return self.__games_by_publisher[publisher]
        except ValueError:
            # No games for specified publisher. Simply return an empty list.
            pass
        return []

    def add_genre(self, genre: Genre):
        if genre not in self.__genres:
            self.__genres.append(genre)

    def get_genres(self) -> List[Genre]:
        return self.__genres

    def add_review(self, review: Review):
        # call parent class first, add_review relies on implementation of code common to all derived classes
        super().add_review(review)
        self.__reviews.append(review)

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


def load_games_from_database(data_path: Path, repo: MemoryRepository):
    games = dict()
    games_filename = str(data_path / "games.csv")

    game_id_column = 0
    game_title_column = 1
    genres_column = 18
    release_date_column = 2
    price_column = 3
    description_column = 4
    image_url_column = 7
    website_url_column = 8
    # reviews_column = 6         #reviews and users not implemented yet/here
    publisher_column = 16

    for data_row in read_csv_file(games_filename):
        # instantiate:
        game_id = int(data_row[game_id_column])
        game = Game(game_id, game_title=data_row[game_title_column])
        # set:
        game.release_date = data_row[release_date_column].strip()
        game.price = float(data_row[price_column].strip())
        game.description = data_row[description_column].strip()
        game.image_url = data_row[image_url_column].strip()
        game.website_url = data_row[website_url_column].strip()
        game.publisher = Publisher(data_row[publisher_column])
        game_genres = data_row[genres_column].strip().split(",") # str to split
        for genre in game_genres:
            game_genre = Genre(genre)
            game.add_genre(game_genre)

        repo.add_game(game)


"""
def load_users(data_path: Path, repo: MemoryRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(
            username=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users
"""

"""
def load_reviews(data_path: Path, repo: MemoryRepository, users):
    reviews_filename = str(Path(data_path) / "reviews.csv")
    for data_row in read_csv_file(reviews_filename):
        review = make_review(
            review_text=data_row[3],
            user=users[data_row[1]],
            game=repo.get_game(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4])
        )
        repo.add_review(review)
"""


def populate(data_path: Path, repo: MemoryRepository):
    # Load games and genres into the repository.
    load_games_from_database(data_path, repo)

    # Load users into the repository.
    #users = load_users(data_path, repo)

    # Load reviews into the repository.
    # load_reviews(data_path, repo, users)

"""
# Demo:

data_path = Path("data")
repo = MemoryRepository()
populate(data_path, repo)

print("Games ID's sorted by their title:", end=5*" ")
for game_id in repo.get_game_ids_sorted_by_title():
    print(f"{game_id} ({repo.get_game(game_id).title})", end=", ")
print()

print("Games with Genre \"Simulation\":", end=5*" ")
for game_id in repo.get_game_ids_by_genre(Genre("Simulation")):
    print(repo.get_game(game_id).title, end=", ")
print()

print("Games released on \"Sep 3, 2015\":", end=5*" ")
for game_id in repo.get_game_ids_on_date("Sep 3, 2015"):
    print(repo.get_game(game_id).title, end=", ")
print()

print("Games released by Publisher \"Aerosoft GmbH\":", end=5*" ")
for game_id in repo.get_game_ids_by_publisher(Publisher("Aerosoft GmbH")):
    print(repo.get_game(game_id).title, end=", ")
print("\nEND - this test repeats twice because __init__.py loads this module on run I think\n")
"""