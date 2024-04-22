from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseSettings
from decouple import config
from typing import List

class Settings(BaseSettings):
    API_V1_STR: str = config('API_V1_STR', default='/api/v1')
    DB_URL: str = config('DB_URL', default='postgresql+asyncpg://postgres:2046@localhost:5432/AppMobile')
    DBBasemodel = declarative_base()

    JWT_SECRET: str = config('JWT_SECRET')
    ALGORITHM: str = 'HS256'

    # Token válido por uma semana => 7 dias
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

settings: Settings = Settings()
