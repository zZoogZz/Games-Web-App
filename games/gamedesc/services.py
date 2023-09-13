from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Review, make_review


class NonExistentGameException(Exception):
	pass


class UnknownUserException(Exception):
	pass


def get_game(game_id: int, repo: AbstractRepository):
	game = repo.get_game(game_id)
	if game is None:
		raise NonExistentGameException

	return game


def add_review(game_id: int, review_text: str, user_name:str, repo: AbstractRepository):
	game = repo.get_game(game_id)
	if game is None:
		raise NonExistentGameException

	user = repo.get_user(user_name)
	if user is None:
		raise UnknownUserException

	review = make_review(review_text, user, game)

	repo.add_review(review)

