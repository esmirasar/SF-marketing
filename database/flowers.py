import sqlite3


def flowers_table(connection: sqlite3.Connection):
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flowers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        schedule INTEGER NOT NULL,
        FOREIGN KEY (user_id)
    REFERENCES users(id)
    )
    ''')

    connection.commit()
