import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent / "database" / "ninjaflow.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection
    