from fastapi import APIRouter

# Importando os endpoints de funcionários e administradores
from api.v1.endpoints import admin

api_router = APIRouter()

# Incluindo o endpoint de administradores
api_router.include_router(
    admin.router, 
    prefix='/admins', 
    tags=['admins']
)

