from core.database import get_connection, close_connection
from utils.hash_password import hash_password
from datetime import datetime

def create_user(user):

    rol_id: int = 1 # 1: Admin
    estado: int = 1 # 1: Activo, 0: Inactivo #Prueba

    # Abrir conexión
    conn = get_connection()

    # Si la conexión es un diccionario significa que retornó un error, manejar error
    if(type(conn) is dict):
        return conn

    try:
        # Cursor: Permite ejecutar comandos SQL en la base de datos a través de la conexión con python.
        cursor = conn.cursor()
        password_hash = hash_password(user.contrasena)
        cursor.execute(
            'INSERT INTO users (nombre, apellido, direccion, username, email, contraseña_hash, rol_id, estado, creado, actualizado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id', 
            (user.nombre, user.apellido, user.direccion, user.username, user.email, password_hash, rol_id, estado, datetime.now(), datetime.now()))

        # Obtener id del usuario creado
        id = cursor.fetchone()[0]

        # Confirmar cambios y cerrar conexión
        conn.commit()
        cursor.close()

        close_connection(conn)

        return id
    except Exception as e:
        # En caso de error, se debe hacer un rollback y cerrar la conexión
        conn.rollback()
        cursor.close()

        close_connection(conn)
        return {'error': str(e)}

def get_users():
    # Obtener registro de usuarios
    return

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