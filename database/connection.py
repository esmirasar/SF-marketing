import os
import psycopg2

from dotenv import load_dotenv


load_dotenv()


def connect_to_postgres():
    db_name = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')

    connection = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    connection.autocommit = True

    return connection
