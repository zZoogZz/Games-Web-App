import csv
from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from games.adapters.repository import AbstractRepository, RepositoryException
from games.domainmodel.model import Game, Genre, Publisher, User, Review, Wishlist


class MemoryRepository: # add (AbstractRepository) and implement remaining functions
    # games ordered by date, not id. id is assumed unique.

    def __init__(self):
        self.__games = dict() #key is game id
        self.__genres = list()
        self.__games_by_genre = dict() #game id's stored against relevant genre
        #self.__games_by_date = dict() #will add later
        self.__users = list()
        self.__reviews = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self.__users if user.username == username), None)

    def add_game(self, game: Game):

        #insort_left(self.__games, game) #dunno what insort_left() does
        if isinstance(game, Game) and game.game_id not in self.__games.keys():
            self.__games[game.game_id] = game

    def get_game_by_id(self, game_id: int) -> Game:
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

    """
    def get_games_by_date(self, target_date: date) -> List[Game]:
        target_game = Game(
            date=target_date,
            title=None,
            first_paragraph=None,
            hyperlink=None,
            image_hyperlink=None
        )
        matching_games = list()

        try:
            index = self.game_index(target_game)
            for game in self.__games[index:None]:
                if game.release_date == target_date:
                    matching_games.append(game)
                else:
                    break
        except ValueError:
            # No games for specified date. Simply return an empty list.
            pass

        return matching_games
    """

    def get_number_of_games(self):
        return len(self.__games)

    def get_first_game(self):
        game = None

        if len(self.__games) > 0:
            game = self.__games[0]
        return game

    def get_last_game(self):
        game = None

        if len(self.__games) > 0:
            game = self.__games[-1]
        return game

    def get_games_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent game ids in the repository.
        existing_ids = [id for id in id_list if id in self.__games_index]

        # Fetch the games.
        games = [self.__games_index[id] for id in existing_ids]
        return games

    def get_game_ids_for_genre(self, genre_name: str):
        return self.__games_by_genre[genre_name]

    """
    # Not sure if get date of game required for us
    def get_date_of_previous_game(self, game: Game):
        previous_date = None

        try:
            index = self.game_index(game)
            for stored_game in reversed(self.__games[0:index]):
                if stored_game.release_date < game.release_date:
                    previous_date = stored_game.release_date
                    break
        except ValueError:
            # No earlier games, so return None.
            pass

        return previous_date

    # Not sure if get date of game required for us

    def get_date_of_next_game(self, game: Game):
        next_date = None

        try:
            index = self.game_index(game)
            for stored_game in self.__games[index + 1:len(self.__games)]:
                if stored_game.release_date > game.release_date:
                    next_date = stored_game.release_date
                    break
        except ValueError:
            # No subsequent games, so return None.
            pass

        return next_date
    """

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
    def game_index(self, game: Game):
        index = bisect_left(self.__games, game)
        if index != len(self.__games) and self.__games[index].release_date == game.release_date:
            return index
        raise ValueError


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
        #instantiate:
        game_id = int(data_row[game_id_column])
        game = Game(game_id, game_title=data_row[game_title_column])
        #set:
        game.release_date = data_row[release_date_column].strip()
        game.price = float(data_row[price_column].strip())
        game.description = data_row[description_column].strip()
        game.image_url = data_row[image_url_column].strip()
        game.website_url = data_row[website_url_column].strip()
        game.publisher = data_row[publisher_column].strip()
        game_genres = data_row[genres_column].strip().split(",") #str to split
        for genre in game_genres:
            game_genre = Genre(genre)
            game.add_genre(game_genre)
            repo.add_genre(game_genre)
            repo.add_game_id_to_genre(game_id, game_genre)

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

#janky tests:
# data_path = Path("data")
# repo = MemoryRepository()
# populate(data_path, repo)
# print(repo.get_game_by_id(951050))
# print(repo.get_game_ids_for_genre(Genre("Action")))


