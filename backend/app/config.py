from dotenv import load_dotenv
import os

load_dotenv()


class Postgres:
    host = "localhost"
    port = "5432"
    database = "antares"
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
