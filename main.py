from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api import users, products, movements, reports, roles

app = FastAPI(title='Inventario de productos', description='API para el manejo de inventario de productos, registros de movimientos, gestión de usuarios y generación de reportes.', version='1.0.0')

app.include_router(users.router, prefix='/users', tags=['Users'])
app.include_router(roles.router, prefix='/roles', tags=['Roles'])
#app.include_router(products.router, prefix='/products', tags=['products'])
#app.include_router(movements.router, prefix='/movements', tags=['movements'])
#app.include_router(reports.router, prefix='/reports', tags=['reports'])

@app.exception_handler(404)
async def not_found(request, exc):
    return JSONResponse(status_code=404, content={'code': 404, 'message': 'Not found'})