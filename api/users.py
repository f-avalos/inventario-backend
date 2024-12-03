from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
# Importar app.services.user_service, se retornan funciones como get_users, get_user_by_id, create_user, update_user, delete_user, etc.
from services import user_service
from utils import hash_password as hashs
from typing import Dict, List, Optional

import re

# Lógica: Para cada método de la API, se debe especificar el tipo de petición (GET, POST, PUT, DELETE), los parámetros que recibe y el tipo de retorno, dentro de cada retorno se debe especificar el código de respuesta y el contenido de la respuesta.

router = APIRouter()

### CRUD USUARIOS

# Clase usuario que representa los datos que debe tener el json con los datos del usuario
class Usuario(BaseModel):
    # el ID se crea automáticamente en la base de datos
    nombre: str
    apellido: str
    direccion: Optional[str]
    username: str
    contrasena: str


    # rol_id, estado, creado y actualizado se asignan en user_service.create_user()

class DisableUsuario(BaseModel):
    usuario_id: int
    disable: bool


# Formato de respuesta de creación de usuario
class UsuarioResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, str]

# Formato de respuesta de error
class ErrorResponse(BaseModel):
    code: int
    message: str
    errors: List[Dict[str, str]]

def validaciones(user: Usuario):

    errors = []

    #Validaciones de datos: verificar si name/email/password son nulos o vacíos, si email es un email válido, etc.
    if(user.nombre is None or user.nombre == ''):
        errors.append({'nombre': 'El nombre es obligatorio'})

    if(user.apellido is None or user.apellido == ''):
        errors.append({'apellido': 'El apellido es obligatorio'})

    if(user.contrasena is None or user.contrasena == ''):
        errors.append({'contrasena': 'La contraseña es obligatoria'})
    if(len(user.contrasena) < 8):
        errors.append({'contrasena': 'La contraseña debe tener al menos 8 caracteres'})

    if(user.username is None or user.username == ''):
        errors.append({'username': 'El campo username es obligatorio'})

    # Fecha creación y actualización se asignan automáticamente en la base de datos

    return errors

## CREATE USER
# se omite escribir /users/register ya que en app/main.py se especifica el prefijo /users
@router.post(
    "/register",
    summary="Registrar usuario",
    description="Genera el registro de un usuario con sus respectivas credenciales y una contraseña encriptada, retorna un mensaje de éxito y la id del usuario creado.",
    responses={
        201: { # Caso de éxito, es 201 porque se crea un nuevo recurso
            "description": "Usuario creado",
            "content": {
                "application/json": {
                    "schema": UsuarioResponse.model_json_schema(),
                    "example": {
                        "code": 201,
                        "message": "El usuario fue creado correctamente",
                        "data": {
                            "id_user": "integer",
                        },
                    
                    }
                }
            }
        },
        400: { # Caso en que los datos enviados no cumplan con las validaciones
            "description": "Error de validaciones de usuario",
            "content": {
                "application/json": {
                    "schema": ErrorResponse.model_json_schema(),
                    "example": {
                        "code": 400,
                        "message": "Error de validaciones",
                        "errors": [
                            {"nombre": "El nombre es obligatorio"},
                            {"apellido": "El apellido es obligatorio"},
                            {"contrasena": "La contraseña es obligatoria"},
                            {"contrasena": "La contraseña debe tener al menos 8 caracteres"},
                            {"username": "El campo username es obligatorio"},

                        ],
                    }
                }
            },
        },
        422: { # Caso en que no se envíen los parámetros requeridos
            "description": "Error de parámetros no ingresados",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "loc": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        },
                                        "msg": {"type": "string"},
                                        "type": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "example": {
                        "detail": [
                            {
                                "type": "missing",
                                "loc": ["body", "value.missing"],
                                "msg": "Field required in body",
                                "input": {"body": "value.missing"}
                            }
                        ]
                    }
                }
            }
        },
        500: {
            "description": "Error de servidor",
            "content": {
                "application/json": {
                    "schema": ErrorResponse.model_json_schema(),
                    "example": {
                        "code": 500,
                        "message": "Error interno del servidor",
                        "errors": "Error al conectar con el servidor o la base de datos"
                    }
                }
            }
        }
    },
)
def register_user(user: Usuario): # Datos que recibe la API desde frontend
    errors = validaciones(user)
    if(len(errors) > 0):
        raise HTTPException(status_code=400, detail={'code': 400, 'message': 'Error de validaciones', 'errors': errors})

    user_response = user_service.create_user(user) # User devolverá la id de usuario creado, se puede retornar la id como respuesta al frontend en caso de que sea necesario

    # Si el user es un diccionario, significa que hubo un error al crear el usuario de parte de la bbdd, se debe retornar un mensaje de error.
    if(type(user_response) is dict):
        return user_response
    
    return {'code': 201, 'message': 'Usuario creado correctamente', 'data': user_response}

# Como la lógica es crear un usuario, se debe llamar a la función create_user del servicio de usuarios, se debe retornar un mensaje de éxito y el usuario creado,

## READ USERS
@router.get('/')
def get_users():
    users = user_service.get_users()

    if(type(users) is dict):
        return users
    
    return {'code': 200,'message': 'Usuarios obtenidos', 'data': users}
'''
## READ USER BY ID
@router.get('/{id}')
def get_user_by_id(id):
    user = get_user_by_id(id)
    if(user is None):
        return {'code': 404, 'message': 'Usuario no encontrado'}
    return {'code': 200, 'data': user}

## UPDATE USER
@router.put('/{id}')
def update_user(id, name, email, password):
    user = update_user(id, name, email, password)
    if(user is None):
        return {'code': 404, 'message': 'Usuario no encontrado'}
    return {'code': 200, 'message': 'Usuario actualizado correctamente', 'data': user}

## DELETE(DISABLE) USER
# Caso particular, desde frontend se envía un booleano para deshabilitar o habilitar al usuario, se debe especificar en la API que se recibe un booleano.
@router.put('/disable/{id}')
def disable_user(id, disable:bool):
    disable_enabled = 'deshabilitado' if disable else 'habilitado'
    user = disable_user(id, disable)
    if(user is None):
        return {'code': 404, 'message': 'Usuario no encontrado'}
    return {'code': 204, 'message': 'Usuario '+disable_enabled+' correctamente', 'data': user}
'''
