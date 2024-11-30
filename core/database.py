# Validaciones y .env
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# BBDD
import mysql.connector
from mysql.connector import pooling


load_dotenv()
class Settings(BaseSettings):
    MYSQL_NAME: str = os.getenv("DATABASE_NAME")
    MYSQL_USER: str = os.getenv("DATABASE_USER")
    MYSQL_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    MYSQL_HOST: str = os.getenv("DATABASE_HOST")
    MYSQL_PORT: str = os.getenv("DATABASE_PORT")

def get_connection():
    try:
        settings = Settings()
        pool = pooling.MySQLConnectionPool(
                pool_name="pool",
                pool_size=10,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                host=settings.MYSQL_HOST,
                database=settings.MYSQL_NAME,
                port=settings.MYSQL_PORT
            )
        conn = pool.get_connection()

        return conn
    except Exception as e:

        return {'code': 500, 'message': 'Error al conectar a la base de datos', 'error': str(e)}

def close_connection(conn):
    conn.close()