import psycopg2
from datetime import datetime

from credentials.database import postgres as p

from queries import CREATE_TABLE_USERS

if __name__ == "__main__":
    try:
        # Create a PostgreSQL database connection.
        connection = psycopg2.connect(
            host=p.host,
            port=p.port,
            database=p.database,
            user=p.user,
            password=p.password,
        )

        with connection.cursor() as cursor:
            cursor.execute(CREATE_TABLE_USERS)

            # Simple insertion test
            query = """INSERT INTO users (username, password, email_address, created_at) VALUES (%s, %s, %s, %s);"""
            data = ("test", "pass", "test@test.com", datetime.now())
            cursor.execute(query, data)
            # Commit to connection to actually "push" the changes to DB.
            connection.commit()

            # Simple selection test
            cursor.execute("SELECT * FROM users;")
            result = cursor.fetchall()
            for row in result: 
                print(row)

    except Exception as e:
        print(f"Something went wrong during Database operations: {e}.")
