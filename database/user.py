def user_table(connection):
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  users (
    id SERIAL PRIMARY KEY,
    telegram_id INTEGER UNIQUE,
    first_name TEXT NOT NULL)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_telegram ON users (telegram_id)
    """)

    cursor.close()
