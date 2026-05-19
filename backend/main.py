from datetime import datetime
from .app.database import create_connection, get_db_cursor, get_engine
from .app.queries import CREATE_TABLE_USERS
from sqlalchemy import text
from pydantic import BaseModel, EmailStr

from fastapi import HTTPException

from fastapi.middleware.cors import CORSMiddleware

# Main entrypoint for fastapi app
from fastapi import FastAPI

# We declare it usually at the top level of our main Python file
app = FastAPI()

class UserRegister(BaseModel):
    username: str
    password: str
    email_address: EmailStr


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

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
def register_user(user_data: UserRegister):
    engine = get_engine()
    insert_query = text("""
        INSERT INTO users (username, password, email_address, created_at) 
        VALUES (:username, :password, :email_address, :created_at)
    """)
    try:
        with engine.begin() as connection:
            connection.execute(insert_query, 
                {
                    "username": user_data.username, 
                    "password": user_data.password,
                    "email_address": user_data.email_address, 
                    "created_at": datetime.now()
                })
            return {"status": "success", "message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")


if __name__ == "__main__":
    main()
