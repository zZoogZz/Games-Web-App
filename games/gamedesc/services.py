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


def add_review(user_name: str, game_id: int, rating: int, review_text: str, repo: AbstractRepository):
	game = repo.get_game(game_id)
	if game is None:
		raise NonExistentGameException

	user = repo.get_user(user_name)
	# if user is None:
	# 	raise UnknownUserException

	review = make_review(user, game, rating, review_text)

	repo.add_review(review)

