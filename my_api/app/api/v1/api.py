from fastapi import APIRouter

# Importando os endpoints de funcionários e administradores
from api.v1.endpoints import funcionario, admin

api_router = APIRouter()

# Incluindo o endpoint de funcionários
api_router.include_router(
    funcionario.router, 
    prefix='/funcionarios', 
    tags=['funcionarios']
)

# Incluindo o endpoint de administradores
api_router.include_router(
    admin.router, 
    prefix='/admins', 
    tags=['admins']
)

