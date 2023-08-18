import csv
from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from games.adapters.repository import AbstractRepository, RepositoryException
from games.domainmodel.model import Game, Genre, Publisher, User, Review, Wishlist


class MemoryRepository(AbstractRepository):
    # games ordered by date, not id. id is assumed unique.

    def __init__(self):
        self.__games = list()
        self.__games_index = dict()
        self.__genres = list()
        self.__users = list()
        self.__reviews = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self.__users if user.username == username), None)

    def add_game(self, game: Game):
        insort_left(self.__games, game) #dunno what insort_left() does
        self.__games_index[game.game_id] = game

    def get_game(self, id: int) -> Game:
        game = None

        try:
            game = self.__games_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return game
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

# * Need to implement function below properly - thinking it needs to search all games and create a new list genre_games
# for those that include that genre.
    def get_game_ids_for_genre(self, genre_name: str):
        # Linear search, to find the first occurrence of a Genre with the name genre_name.
        genre = next((genre for genre in self.__genres if genre.genre_name == genre_name), None)

        # Retrieve the ids of games associated with the Genre.
        if genre is not None:
            game_ids = [game.game_id for game in genre.genre_games]  #* no such thing as genre_games list yet
        else:
            # No Genre with name genre_name, so return an empty list.
            game_ids = list()

        return game_ids
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

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_games_and_genres(data_path: Path, repo: MemoryRepository):
    genres = dict()

    games_filename = str(data_path / "news_games.csv")
    for data_row in read_csv_file(games_filename):

        game_key = int(data_row[0]) # * check columns!!
        number_of_genres = len(data_row) - 6
        game_genres = data_row[-number_of_genres:]

        # Add any new genres; associate the current game with genres.
        for genre in game_genres:
            if genre not in genres.keys():
                genres[genre] = list()
            genres[genre].append(game_key)
        del data_row[-number_of_genres:]

        # Create game object.
        game = Game(
            # use setter: release_date=date.fromisoformat(data_row[1]),
            game_id=game_key,  # game_key?
            game_title=data_row[2]
            #first_paragraph=data_row[3],
            #hyperlink=data_row[4],
            #image_hyperlink=data_row[5],
        )

        # Add the game to the repository.
        repo.add_game(game)

    # Create Genre objects, associate them with games and add them to the repository.
    for genre_name in genres.keys():
        genre = Genre(genre_name)
        for game_id in genres[genre_name]:
            game = repo.get_game(game_id)
            make_genre_association(game, genre)
        repo.add_genre(genre)


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


def populate(data_path: Path, repo: MemoryRepository):
    # Load games and genres into the repository.
    load_games_and_genres(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load reviews into the repository.
    load_reviews(data_path, repo, users)
