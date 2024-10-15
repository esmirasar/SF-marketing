import psycopg2

from dotenv import load_dotenv
from bot.config import config


load_dotenv()


def connect_to_postgres():
    db_name = config.DB_NAME
    user = config.DB_USER
    password = config.DB_PASSWORD
    host = config.DB_HOST
    port = config.DB_PORT

    connection = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    connection.autocommit = True

    return connection
