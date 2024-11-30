from core.database import get_connection, close_connection

def create_role(rol):
    conn = get_connection()

    if(type(conn) is dict):
        return conn
    
    try:
        cursor = conn.cursor()

        # Insertar rol
        query = 'INSERT INTO rol (nombre) VALUES (%s)'
        data = (rol.nombre,)
        cursor.execute(query, data)

        # Obtener id del rol y recuperar el nombre
        role = cursor.lastrowid
        cursor.execute(
            'SELECT nombre FROM rol WHERE rol_id = %s', (role,)
        )
        nombre = cursor.fetchone()[0]

        conn.commit()
        return nombre
    except Exception as e:
        conn.rollback()
        return {'code': 500, 'message': 'Error al crear el rol', 'error': str(e)}
    finally:
        if cursor:
            cursor.close()
        if conn:
            close_connection(conn)