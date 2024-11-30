from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services import role_service

router = APIRouter()

class Rol(BaseModel):
    nombre: str

class ErrorResponse(BaseModel):
    code: int
    message: str

# CREATE ROLE
@router.post(
    '/create',
    tags=['Roles'],
    summary='Crear un nuevo rol',
    description='Genera el registro de un nuevo rol en la base de datos, retorna un mensaje de éxito y el nombre del rol creado.',
    responses={
        201: {
            'description': 'Rol creado exitosamente',
            'content': {
                'application/json': {
                    "schema": Rol.model_json_schema(),
                    'example': {
                        'code': 201,
                        'message': 'Rol creado exitosamente',
                        'data': {
                            'nombre': 'string'
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Error al crear el rol',
            'content': {
                'application/json': {
                    'schema': ErrorResponse.model_json_schema(),
                    'example': {
                        'code': 400,
                        'message': 'El nombre del rol debe ser obligatorio'
                    }
                }
            }
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
                        "errors": "Error al conectar con el servidor hacia la base de datos"
                    }
                }
            }
        }
    })
def create_role(rol: Rol):
    if(rol.nombre == ''):
        raise HTTPException(status_code=400, detail={'code': 400, 'message': 'Error de validaciones', 'errors': {'nombre': 'El nombre del rol es obligatorio'}})

    nuevo_rol = role_service.create_role(rol)

    if(type(nuevo_rol) is dict):
        raise HTTPException(status_code=500, detail=nuevo_rol)
    
    return {'code': 201, 'message': 'Rol creado exitosamente', 'data': {'nombre': nuevo_rol}}