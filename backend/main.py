from datetime import datetime
from app.database import create_connection, get_db_cursor, get_engine
from app.queries import CREATE_TABLE_USERS
from sqlalchemy import text


def main():
    # First way
    connection = create_connection()

    if not connection:
        raise Exception("error 404")

    with connection.cursor() as cursor:
        cursor.execute(CREATE_TABLE_USERS)

        query = """INSERT INTO users (username, password, email_address, created_at) VALUES (%s, %s, %s, %s);"""
        data = ("test1", "pass", "test1@test.com", datetime.now())
        cursor.execute(query, data)
        connection.commit()

        cursor.execute("SELECT * FROM users;")
        result = cursor.fetchall()
        for row in result:
            print(row)
    # Second way
    with get_db_cursor() as cursor:
        cursor.execute(CREATE_TABLE_USERS)

        query = """INSERT INTO users (username, password, email_address, created_at) VALUES (%s, %s, %s, %s);"""
        data = ("test2", "pass", "test2@test.com", datetime.now())
        cursor.execute(query, data)

        cursor.execute("SELECT * FROM users;")
        result = cursor.fetchall()
        for row in result:
            print(row)
    # Third way
    engine = get_engine()
    with engine.connect() as cursor:
        cursor.execute(text(CREATE_TABLE_USERS))

        # query = """INSERT INTO users (username, password, email_address, created_at) VALUES (%s, %s, %s, %s);"""
        # data = ("test", "pass", "test@test.com", datetime.now())
        # cursor.execute(text(query), data)

        result = cursor.execute(text("SELECT * FROM users;"))
        # result = cursor.fetchall()
        for row in result:
            print(row)


if __name__ == "__main__":
    main()
