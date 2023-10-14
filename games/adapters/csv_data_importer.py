import csv
from pathlib import Path
from datetime import date, datetime

from werkzeug.security import generate_password_hash

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, User, Review, make_review

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

def load_users(data_path: Path, repo: AbstractRepository):
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


def load_reviews(data_path: Path, repo: AbstractRepository, users):
    comments_filename = str(Path(data_path) / "reviews.csv")
    for data_row in read_csv_file(comments_filename):
        comment = make_review(
            user=users[data_row[1]],
            game=repo.get_game(int(data_row[2])),
            rating=int(data_row[4]),
            review_text=data_row[3]
        )
        repo.add_review(comment)
