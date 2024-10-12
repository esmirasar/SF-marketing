from dotenv import load_dotenv

from connection import connect_to_postgres
from user import user_table
from flowers import flowers_table


load_dotenv()

if __name__ == '__main__':
    connection = connect_to_postgres()

    user_table(connection)
    flowers_table(connection)

    connection.close()
