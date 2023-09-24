from flask import session
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, User, make_review, remove_review
import games.adapters.repository as repo


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
	if user is None:
		raise UnknownUserException

	existing_review = get_existing_review(game, user_name)

	if existing_review is not None:
		remove_review(user, game, existing_review)
		repo.remove_review(existing_review)

	review = make_review(user, game, rating, review_text)

	repo.add_review(review)


def get_existing_review(game: Game, user_name: str):

	user = repo.repo_instance.get_user(user_name)
	if user is not None:
		for review in user.reviews:
			if review.game == game:
				return review
	return None



