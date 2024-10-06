import sqlite3


def user_table(connection: sqlite3.Connection):
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  users (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER,
    first_name TEXT NOT NULL)
    """)

    cursor.execute("""
    CREATE INDEX idx_telegram ON users (telegram_id)
    """)

    connection.commit()
