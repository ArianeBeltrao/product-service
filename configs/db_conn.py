import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_database_connection():
    db_connection = psycopg2.connect(
        database=os.getenv("DATABASE_NAME"),
        host=os.getenv("DATABASE_HOST"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        port=os.getenv("DATABASE_PORT"),
    )
    return db_connection
