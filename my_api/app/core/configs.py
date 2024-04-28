from sqlalchemy.ext.declarative import declarative_base
from pydantic_settings import BaseSettings
from decouple import config
from typing import List, ClassVar
import secrets

class Settings(BaseSettings):
    API_V1_STR: str = config('API_V1_STR', default='/api/v1')
    DB_URL: str = config('DB_URL', default='postgresql+asyncpg://postgres:2046@localhost:5432/AppMobile')
    
    DBBasemodel: ClassVar = declarative_base()

    jwt_secret_default: ClassVar[str] = secrets.token_hex(32)

    JWT_SECRET: str = config('JWT_SECRET', default=jwt_secret_default)
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

settings: Settings = Settings()



