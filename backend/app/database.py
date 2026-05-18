from app.config import Postgres as p
from psycopg2.extensions import connection
import psycopg2, contextlib
from sqlalchemy import create_engine, URL


def get_engine():
    url_object = URL.create(
        "postgresql+psycopg2",
        username=p.user,
        password=p.password,  # plain (unescaped) text
        host=p.host,
        database=p.database,
    )

    return create_engine(url_object)


def create_connection() -> connection | None:
    try:
        # Create a PostgreSQL database connection.
        connection = psycopg2.connect(
            host=p.host,
            port=p.port,
            database=p.database,
            user=p.user,
            password=p.password,
        )
        return connection
    except Exception as e:
        print(f"Something went wrong during Database operations: {e}.")


@contextlib.contextmanager
def get_db_cursor():
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(
            host=p.host,
            port=p.port,
            database=p.database,
            user=p.user,
            password=p.password,
        )

        cursor = connection.cursor()
        yield cursor
        connection.commit()

    except Exception as e:
        print(f"Something went wrong during Database operations: {e}.")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
