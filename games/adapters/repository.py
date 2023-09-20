import abc
from typing import List
# from datetime import date

from games.domainmodel.model import Game, Genre, Publisher, User, Review, Wishlist


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_game(self, game: Game):
        """ Adds an Game to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_game(self, game_id: int) -> Game:
        """ Returns Game with id from the repository.

        If there is no Game with the given id, this method returns None.
        """
        raise NotImplementedError

    def get_games(self):
        """ Gets the dictionary of all games in repo """
        raise NotImplementedError

    def get_game_ids(self):
        """ Gets the game ids of all games in repo """
        raise NotImplementedError


    @abc.abstractmethod
    def add_game_id_to_genre(self, game_id: int, genre: Genre):
        """ Adds adds game id against genre key in games by genre dictionary. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_game_id_to_release_date(self, game_id: int, release_date: str):
        """ Adds game id against date key in games by date dictionary. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_game_id_to_publisher(self, game_id: int, publisher: Publisher):
        """ Adds game id against publisher key in games by publisher dictionary. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_ids_on_date(self, release_date: str) -> List[int]:
        """ Gets list of game ids released on that date. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self) -> int:
        """ Returns the number of Games in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_ids(self, id_list):
        """ Returns a list of Games, whose ids match those in id_list, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_ids_by_genre(self, genre: Genre):
        """ Returns a list of game ids which are associated with a Genre.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_ids_sorted_by_title(self) -> List[int]:
        """ Returns a list of all game id's sorted according to game title.
        """

    @abc.abstractmethod
    def get_sorted_release_dates(self):
        """ Returns a list of all dates (as strings) on which a game in the games dictionary has a release date,
        sorted as datetime objects.

        If there are no matches, this method returns an empty list.
        """

    @abc.abstractmethod
    def get_previous_release_date(self, game: Game):
        """ Returns the previous release date in the repository
        Returns None if an invalid release date (not formatted or not in the repository) is passed
        Returns None if no earlier release dates in repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_release_date(self, release_date:str):
        """ Returns the next release date in the repository
        Returns None if an invalid release date (not formatted or not in the repository) is passed
        Returns None if no later release dates in repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a Genre to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns the Genres stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with an Game and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.game is None or review not in review.game.reviews:
            raise RepositoryException('Review not correctly attached to an Game')

    @abc.abstractmethod
    def remove_review(self, review: Review):
        """ Removes a review from the repository, if present. """

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError







