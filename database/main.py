import psycopg2
import os

from dotenv import load_dotenv

from user import user_table
from flowers import flowers_table


load_dotenv()

db_name = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

if __name__ == '__main__':
    connection = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    connection.autocommit = True

    user_table(connection)
    flowers_table(connection)

    connection.close()
