def flowers_table(connection):
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flowers(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    schedule INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id))
    """)

    cursor.close()
