from core.database import get_connection, close_connection
from utils.hash_password import hash_password

def create_user(user):

    # Abrir conexión
    conn = get_connection()

    # Si la conexión es un diccionario significa que retornó un error, manejar error
    if(type(conn) is dict):
        return conn

    try:
        with conn.cursor() as cursor:

            password_hash = hash_password(user.contrasena)

            cursor.execute(
            'INSERT INTO usuario (nombre, apellido, direccion, username, password_hash) VALUES (%s, %s, %s, %s, %s) RETURNING usuario_id', 
            (user.nombre, user.apellido, user.direccion, user.username, password_hash))
            user_id = cursor.fetchone()[0]
            conn.commit()
            return user_id
    except Exception as e:
        # En caso de error, se debe hacer un rollback y cerrar la conexión
        conn.rollback()
        return {'code': 500, 'message': 'Error al crear usuario', 'error': str(e)}
    finally:
        if cursor:
            cursor.close()
        if conn:
            close_connection(conn)

def get_users():
    # Abrir conexión
    conn = get_connection()
    # Si la conexión es un diccionario significa que retornó un error, manejar error
    if(type(conn) is dict):
        return conn
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM usuario;')
        users = cursor.fetchall()

        cursor.close()
        close_connection(conn)
        return users
    except Exception as e:
        return {'code': 500, 'message': 'Error al obtener usuarios', 'error': str(e)}
    finally:
        if cursor:
            cursor.close()
        if conn:
            close_connection(conn)


def get_user_by_id(id):
    # Obtener usuario por id
    return

def update_user(id, name, email, password):
    # Actualizar usuario
    return

def disable_user(id, disable):
    # Deshabilitar usuario
    # Si disable es True, deshabilitar usuario
    # Si disable es False, habilitar usuario
    return