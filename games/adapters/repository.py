import abc
from typing import List
from datetime import date

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
    def get_game(self, id: int) -> Game:
        """ Returns Game with id from the repository.

        If there is no Game with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_date(self, target_date: date) -> List[Game]:
        """ Returns a list of Games that were published on target_date.

        If there are no Games on the given date, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self) -> int:
        """ Returns the number of Games in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_game(self) -> Game:
        """ Returns the first Game, ordered by date, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_game(self) -> Game:
        """ Returns the last Game, ordered by date, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_id(self, id_list):
        """ Returns a list of Games, whose ids match those in id_list, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_ids_for_genre(self, genre_name: str):
        """ Returns a list of ids representing Games that are genreged by genre_name.

        If there are Games that are genreged by genre_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_date_of_previous_game(self, game: Game):
        """ Returns the date of an Game that immediately precedes game.

        If game is the first Game in the repository, this method returns None because there are no Games
        on a previous date.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_date_of_next_game(self, game: Game):
        """ Returns the date of an Game that immediately follows game.

        If game is the last Game in the repository, this method returns None because there are no Games
        on a later date.
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
    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError







