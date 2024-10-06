import sqlite3


connection = sqlite3.connect('tg_bot.db')

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

connection.close()
