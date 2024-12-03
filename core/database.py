# Validaciones y .env
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# BBDD
import psycopg2
from psycopg2.extras import RealDictCursor


load_dotenv()
class Settings(BaseSettings):
    POSTGRESQL_NAME: str = os.getenv("DATABASE_NAME")
    POSTGRESQL_USER: str = os.getenv("DATABASE_USER")
    POSTGRESQL_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    POSTGRESQL_HOST: str = os.getenv("DATABASE_HOST")
    POSTGRESQL_PORT: str = os.getenv("DATABASE_PORT")

def get_connection():
    try:
        settings = Settings()
        conn = psycopg2.connect(
            dbname=settings.POSTGRESQL_NAME,
            user=settings.POSTGRESQL_USER,
            password=settings.POSTGRESQL_PASSWORD,
            host=settings.POSTGRESQL_HOST,
            port=settings.POSTGRESQL_PORT,
            cursor_factory=RealDictCursor
        )

        return conn
    except Exception as e:
        return {'code': 500, 'message': 'Error al conectar a la base de datos', 'error': str(e)}

def close_connection(conn):
    conn.close()