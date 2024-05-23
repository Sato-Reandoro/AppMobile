from lib2to3.pytree import Base
from core.configs import settings
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Column,
    Boolean
)

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Column,
    Boolean
)

class UsuarioModel(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256), nullable=True)
    sobrenome = Column(String(256), nullable=True)
    email = Column(String(256), index=True, nullable=False, unique=True)
    hashed_password = Column(String(256), nullable=False)  # Novo campo para armazenar o hash da senha
    eh_admin = Column(Boolean, default=False)
    tipo_usuario = Column(String(256), nullable=True, default='usuario')

