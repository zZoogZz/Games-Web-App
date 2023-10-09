from abc import ABC

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound


from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Publisher, Genre, User, Review


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        """ Adds a User to the repository. """
        raise NotImplementedError

    def check_username_unique(self, username: str):
        """ Checks if username is unique, regardless of case. """
        raise NotImplementedError

    def get_user(self, user_name) -> User:
        """
        Returns the User named user_name from the repository.
        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    def add_game(self, game: Game):
        """
        Adds a game to the repository.
        """
        with self._session_cm as scm:
            # TODO: This doesn't work..............
            self._session_cm.session.merge(game)
            self._session_cm.session.commit()

    def get_game(self, game_id: int) -> Game:
        """
        Returns Game with id from the repository.
        If there is no Game with the given id, this method returns None.
        """
        try:
            return self._session_cm.session.query(Game).filter(Game._Game__game_id == game_id).one()
        except NoResultFound:
            return None

    def get_games(self):
        """ Gets the dictionary of all games in repo """
        games = self._session_cm.session.query(Game).order_by(Game._Game__game_id).all()

        gamedict = {}
        for game in games:
            gamedict[game.game_id] = game

        return gamedict

    def get_game_ids(self):
        """ Gets the game ids of all games in repo """
        return self.get_games().keys()


    def add_game_id_to_genre(self, game_id: int, genre: Genre):
        """ Adds adds game id against genre key in games by genre dictionary. """
        raise NotImplementedError

    def add_game_id_to_release_date(self, game_id: int, release_date: str):
        """ Adds game id against date key in games by date dictionary. """
        raise NotImplementedError

    def add_game_id_to_publisher(self, game_id: int, publisher: Publisher):
        """ Adds game id against publisher key in games by publisher dictionary. """
        raise NotImplementedError

    def get_game_ids_on_date(self, release_date: str) -> list[int]:
        """ Gets list of game ids released on that date. """
        raise NotImplementedError

    def get_number_of_games(self) -> int:
        """ Returns the number of Games in the repository. """
        raise NotImplementedError

    def get_games_by_ids(self, id_list):
        """
        Returns a list of Games, whose ids match those in id_list, from the repository.
        If there are no matches, this method returns an empty list.
        """
        game_list = []

        if id_list:
            for game_id in id_list:

                game = self.get_game(game_id)

                if game:
                    game_list.append(game)

        return game_list

    def get_game_ids_by_genre(self, genre: Genre):
        """ Returns a list of game ids which are associated with a Genre.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    def get_game_ids_sorted_by_title(self) -> list[int]:
        """ Returns a list of all game id's sorted according to game title.
        """

    def get_sorted_release_dates(self):
        """ Returns a list of all dates (as strings) on which a game in the games dictionary has a release date,
        sorted as datetime objects.

        If there are no matches, this method returns an empty list.
        """

    def get_previous_release_date(self, game: Game):
        """ Returns the previous release date in the repository
        Returns None if an invalid release date (not formatted or not in the repository) is passed
        Returns None if no earlier release dates in repository.
        """
        raise NotImplementedError

    def get_next_release_date(self, release_date:str):
        """ Returns the next release date in the repository
        Returns None if an invalid release date (not formatted or not in the repository) is passed
        Returns None if no later release dates in repository.
        """
        raise NotImplementedError

    def add_genre(self, genre: Genre):
        """ Adds a Genre to the repository. """
        with self._session_cm as scm:
            self._session_cm.session.merge(genre)
            self._session_cm.session.commit()

    def add_publisher(self, publisher: Publisher):
        """ Adds a Publisher to the repository. """
        with self._session_cm as scm:
            self._session_cm.session.merge(publisher)
            self._session_cm.session.commit()

    def get_genres(self) -> list[Genre]:
        """ Returns the Genres stored in the repository. """
        raise NotImplementedError

    def add_review(self, review: Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with an Game and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        raise NotImplementedError
    def remove_review(self, review: Review):
        """ Removes a review from the repository, if present. """

    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError

    def game_is_favourite(self, game: Game, user: User):
        """ Checks if the game is a favourite. """
        raise NotImplementedError

    def get_favourites(self, user: User):
        """ Returns the favourite games for a user that are stored in the repository. """
        raise NotImplementedError

    def toggle_favourite(self, game: Game, user: User):
        """ Toggles a game's favourite status. """
        raise NotImplementedError

