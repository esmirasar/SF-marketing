import sqlite3

from user import user_table
from flowers import flowers_table


if __name__ == '__main__':
    connection = sqlite3.connect('tg_bot.db')
    user_table(connection)
    flowers_table(connection)
    connection.close()
