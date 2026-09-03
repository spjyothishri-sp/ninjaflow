import sqlite3

DATABASE = "database/ninjaflow.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection