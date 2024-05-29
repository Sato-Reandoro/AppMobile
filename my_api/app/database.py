<<<<<<< Updated upstream:my_api/app/core/database.py
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
=======
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:2046@localhost:5432/AppMobile"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
>>>>>>> Stashed changes:my_api/app/database.py
