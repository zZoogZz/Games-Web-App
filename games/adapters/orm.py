from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Text, Float, ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from games.domainmodel.model import Game, Publisher, Genre, User, Review

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

# TODO: Create Tables here


def map_model_to_tables():
    # TODO: Create Model/Table mappings here

    pass
