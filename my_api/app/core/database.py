from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.configs import settings

# Atualizando a URL do banco de dados para a fornecida
settings.DB_URL = "postgresql+asyncpg://postgres:2046@localhost:5432/AppMobile"

# Criando o motor de banco de dados assíncrono
engine: AsyncEngine = create_async_engine(settings.DB_URL)

# Criando a fábrica de sessões assíncronas
Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)
