from sqlalchemy import select, inspect

from games.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['game_genres', 'games', 'reviews', 'genres', 'users']

def test_database_populate_select_all_genres(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table genres
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['genre_name'])

        assert all_genre_names == ['Action', 'Indie', 'a', 'b']

def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['thorke', 'fmercury']

def test_database_populate_select_all_reviews(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table reviews
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append((row['id'], row['user_id'], row['game_id'], row['review']))

        assert all_reviews == [(1, 2, 1, 'Oh no, COVID-19 has hit New Zealand'),
                                (2, 1, 1, 'Yeah Freddie, bad news')]

def test_database_populate_select_all_games(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_games_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table games
        select_statement = select([metadata.tables[name_of_games_table]])
        result = connection.execute(select_statement)

        all_games = []
        for row in result:
            all_games.append((row['id'], row['title']))

        nr_games = len(all_games)
        assert nr_games == 6

        assert all_games[0] == (1, 'Coronavirus: First case of virus in New Zealand')
