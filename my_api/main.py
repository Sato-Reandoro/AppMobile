from core.configs import settings
from api.v1.api import api_router
from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path

# Adiciona o diretório atual ao caminho de busca do Python
sys.path.append(str(Path(__file__).resolve().parent))



app = FastAPI(title='FastAPI | PostgreSQL e JWT - Segurança - Kevin Soffa')
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_level='info',
        reload=True
    )
