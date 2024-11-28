# Validaciones y .env
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# BBDD
import psycopg2

load_dotenv()
class Settings(BaseSettings):
    POSTGRES_NAME: str = os.getenv("DATABASE_NAME")
    POSTGRES_USER: str = os.getenv("DATABASE_USER")
    POSTGRES_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    POSTGRES_HOST: str = os.getenv("DATABASE_HOST")
    POSTGRES_PORT: str = os.getenv("DATABASE_PORT")


def get_connection():
    try:
        settings = Settings()
        conn = psycopg2.connect(
            dbname=settings.POSTGRES_NAME,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT
        )
        return conn
    except Exception as e:

        return {'code': 500, 'message': 'Error al conectar a la base de datos', 'error': str(e)}

def close_connection(conn):
    conn.close()