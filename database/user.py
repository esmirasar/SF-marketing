def user_table(connection):
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE,
    first_name VARCHAR(255) NOT NULL,
    time_zone VARCHAR(100) NOT NULL)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_telegram ON users (telegram_id)
    """)

    cursor.close()
