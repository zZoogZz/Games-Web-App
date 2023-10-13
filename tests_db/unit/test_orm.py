"""
Adapted from CS235-S2-2023-CovidWebApp
"""

import pytest

from datetime import datetime

from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import User, Game, Review, Genre, make_review, remove_review  # make_genre_association


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT username from users where username = :username',
                                {'username': new_name}).fetchone()
    print("insert user returns:")
    print(row[0])
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT username from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_game(empty_session):
    empty_session.execute(
        'INSERT INTO games (game_id, game_title, release_date, game_price, game_description, game_image_url, game_website_url, publisher_name) VALUES '
        '(7940, "Call of DutyÂ® 4: Modern WarfareÂ®", :release_date, 9.99, "The new action-thriller...", '
        '"https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118", '
        '"http://www.charlieoscardelta.com/", "Activision")',
        {'release_date': "Nov 12, 2007"}
    )
    row = empty_session.execute('SELECT game_id from games').fetchone()
    print("insert game returns:")
    print(row[0])
    return row[0]


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (name) VALUES ("Action"), ("Indie")'
    )
    rows = list(empty_session.execute('SELECT name from genres'))  # ###
    keys = tuple(row[0] for row in rows)
    return keys


def insert_game_genre_associations(empty_session, game_key, genre_keys):
    stmt = 'INSERT INTO game_genre (game, genre) VALUES (:game, :genre)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'game': game_key, 'genre': genre_key})


def insert_reviewed_game(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session)

    empty_session.execute(
        'INSERT INTO reviews (user, game, rating, comment) VALUES '
        '(:username, :game, :rating1, "Review 1"),'
        '(:username, :game, :rating2, "Review 2")',
        {'username': user_key, 'game': game_key, 'rating1': 3, 'rating2': 4}
    )

    row = empty_session.execute('SELECT game_id from games').fetchone()
    return row[0]


def make_game():
    game = Game(7940,"Call of Duty® 4: Modern Warfare®")
    game.price = 9.99
    game.release_date = "Nov 12, 2007"
    game.description = "The new action-thriller..."
    game.image_url = "https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118"
    game.website_url = "http://www.charlieoscardelta.com/"
    return game


def make_user():
    user = User("andrew", "Abcde1234")
    return user


def make_genre():
    genre = Genre("Action")
    return genre


def test_loading_of_users(empty_session):
    users = list()
    users.append(("andrew", "Abcde1234"))
    users.append(("cindy", "Abcde1111"))
    insert_users(empty_session, users)

    expected = [
        User("andrew", "Abcde1234"),
        User("cindy", "Abcde1111")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("andrew", "Abcde1234")]


def test_saving_of_users_with_common_username(empty_session):
    insert_user(empty_session, ("andrew", "Abcd1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("andrew", "Abcde111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_game(empty_session):
    game_key = insert_game(empty_session)
    expected_game = make_game()
    fetched_game = empty_session.query(Game).one()

    assert expected_game == fetched_game
    assert game_key == fetched_game.game_id


def test_loading_of_genred_game(empty_session):
    game_key = insert_game(empty_session)
    genre_keys = insert_genres(empty_session)
    insert_game_genre_associations(empty_session, game_key, genre_keys)

    game = empty_session.query(Game).get(game_key)
    genres = [empty_session.query(Genre).get(key) for key in genre_keys]

    for genre in genres:
        assert genre in game.genres


def test_loading_of_reviewed_game(empty_session):
    insert_reviewed_game(empty_session)

    rows = empty_session.query(Game).all()
    game = rows[0]

    for review in game.reviews:
        assert review.game is game


def test_saving_of_review(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session, ("andrew", "Abcde1234"))

    rows = empty_session.query(Game).all()
    game = rows[0]
    user = empty_session.query(User).filter(User._User__username == "andrew").one()

    # Create a new Review that is bidirectionally linked with the User and Game.
    review_text = "Some review text."
    review = make_review(user, game, 3, review_text)

    # Note: if the bidirectional links between the new Review and the User and
    # Game objects hadn't been established in memory, they would exist following
    # committing the addition of the Review to the database.
    empty_session.add(review)
    empty_session.commit()

    test_rows = empty_session.query(Review).all()
    for review in test_rows:
        print("review in test_rows: ", review)
        print("review.user", review.user)
        print("review.game", review.game)
        print("review.comment", review.comment)

    rows = list(empty_session.execute('SELECT * FROM reviews'))
    print("test_saving_of_review rows:", rows)

    assert rows == [(user_key, game_key, review_text)]


def test_saving_of_game(empty_session):
    game = make_game()
    empty_session.add(game)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT game_id, game_title, game_price, release_date, game_description, game_image_url, game_website_url FROM games'))
    release_date = "Nov 12, 2007"
    assert rows == [(7940, "Call of Duty® 4: Modern Warfare®", 9.99, release_date,
                     "The new action-thriller...",
                     "https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118",
                     "http://www.charlieoscardelta.com/"
                     )]


def test_saving_genred_game(empty_session):
    game = make_game()
    genre = make_genre()

    # Establish the bidirectional relationship between the Game and the Genre.
    game.add_genre(genre)


    # Persist the Game (and Genre).
    # Note: it doesn't matter whether we add the Genre or the Game. They are connected
    # bidirectionally, so persisting either one will persist the other.
    empty_session.add(game)
    empty_session.commit()

    # Test test_saving_of_game() checks for insertion into the games table.
    rows = list(empty_session.execute('SELECT game_id FROM games'))
    game_key = rows[0][0]

    # Check that the genres table has a new record.
    rows = list(empty_session.execute('SELECT name FROM genres'))
    genre_key = rows[0][0]
    assert rows[0][0] == "Action"

    # Check that the game_genre table has a new record.
    rows = list(empty_session.execute('SELECT game, genre from game_genre'))
    game_foreign_key = rows[0][0]
    genre_foreign_key = rows[0][1]

    assert game_key == game_foreign_key
    assert genre_key == genre_foreign_key


def test_save_reviewed_game(empty_session):
    # Create Game User objects.
    game = make_game()
    user = make_user()

    # Create a new Review that is bidirectionally linked with the User and Game.
    review_text = "Some review text."
    review = make_review(user, game, 3, review_text)

    # Save the new Game.
    empty_session.add(game)
    empty_session.commit()

    # Test test_saving_of_game() checks for insertion into the games table.
    rows = list(empty_session.execute('SELECT game_id FROM games'))
    game_key = rows[0][0]

    # Test test_saving_of_users() checks for insertion into the users table.
    rows = list(empty_session.execute('SELECT username FROM users'))
    user_key = rows[0][0]

    # Check that the reviews table has a new record that links to the games and users
    # tables.
    rows = list(empty_session.execute('SELECT user, game, comment FROM reviews'))

    print(rows)

    assert rows == [(user_key, game_key, review_text)]