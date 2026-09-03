import sqlite3
import os

DATABASE = os.path.join(
    os.path.dirname(__file__),
    "database",
    "ninjaflow.db"
)


def get_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection