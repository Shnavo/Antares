import psycopg2
from datetime import datetime
from credentials.database import postgres as p

if __name__ == "__main__":
    try:
        connection = psycopg2.connect(
            host=p.host,
            port=p.port,
            database=p.database,
            user=p.user,
            password=p.password,
        )
        cursor = connection.cursor()
        query = "INSERT INTO users (username, password, email_address, created_at) VALUES (%s, %s, %s, %s);"
        data = ("test", "pass", "test@test.com", datetime.now())
        cursor.execute(query, data)
        cursor.execute("SELECT * FROM users;")
        connection.commit()
        result = cursor.fetchall()
        print(result)
    except Exception as e:
        print(e)
