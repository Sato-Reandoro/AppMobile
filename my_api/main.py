import sys
from pathlib import Path

app_path = Path(__file__).resolve().parent
app_directory = app_path / 'app'
sys.path.append(str(app_directory))

from core.configs import settings

from api.v1.api import api_router
from fastapi import FastAPI
import uvicorn

app = FastAPI(title='FastAPI | PostgreSQL e JWT - Segurança -')
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_level='info',
        reload=True
    )
    
    