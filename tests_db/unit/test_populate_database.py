from sqlalchemy import select, inspect

from games.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):
    """
    Tests all expected tables exist with correct names in test databaes.
    """
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['game_genre', 'games', 'genres', 'publishers', 'reviews',
                                           'users', 'users_favourites']

def test_database_populate_select_all_genres(database_engine):
    """
    Tests genres table populates and all genres from test games.csv can be retrieved.
    """
    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table genres
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['name'])

        assert sorted(all_genre_names) == ['Action', 'Test-Genre']

def test_database_populate_select_all_users(database_engine):
    """
    Tests users table populates and all users from test users.csv can be retrieved.
    """
    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['username'])

        assert all_users == ['spork', 'jazzman']

def test_database_populate_select_all_reviews(database_engine):
    """
    Tests reviews table populated and all reviews can be retrieved.
    """
    # Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table reviews
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append((row['review_id'], row['user'], row['game'], row['rating'], row['comment']))

        assert all_reviews == [(1, 'jazzman', 7940, 2, 'Wow, this is Call of Duty.'),
                                (2, 'spork', 418650, 4, 'Pirates pirates pirates.')]

def test_database_populate_select_all_games(database_engine):
    """
    Tests that games table is populated with all games in test games.csv
    """
    # Get table information
    inspector = inspect(database_engine)
    name_of_games_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table games
        select_statement = select([metadata.tables[name_of_games_table]])
        result = connection.execute(select_statement)

        all_games = []
        for row in result:
            all_games.append((row['game_id'], row['game_title']))

        nr_games = len(all_games)
        assert nr_games == 5

        assert all_games[0] == (7940, 'Call of Duty® 4: Modern Warfare®')

def test_database_populate_select_favourites(database_engine):
    """
    Tests that favourites table is populated (using test favourites in user_favourites.csv).
    """

    # Get table information
    inspector = inspect(database_engine)
    name_of_favourites_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # query for records in table reviews
        select_statement = select([metadata.tables[name_of_favourites_table]])
        result = connection.execute(select_statement)

        all_favourites = []
        for row in result:
            all_favourites.append((row['username'], row['favourite_game']))

        assert all_favourites == [('spork', 7940),
                                ('spork', 418650)]