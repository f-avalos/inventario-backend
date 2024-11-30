from core.database import get_connection, close_connection
from utils.hash_password import hash_password

def create_user(user):

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
            'INSERT INTO usuario (nombre, apellido, direccion, username, password_hash) VALUES (%s, %s, %s, %s, %s)', 
            (user.nombre, user.apellido, user.direccion, user.username, password_hash))
        
        user_id = cursor.lastrowid

        cursor.execute(
            'SELECT usuario_id FROM usuario WHERE usuario_id = %s', (user_id,)
        )

        # Obtener id del usuario creado
        id = cursor.fetchone()[0]

        # Confirmar cambios y cerrar conexión
        conn.commit()

        return id
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