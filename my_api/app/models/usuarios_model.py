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

class UsuarioModel(settings.DBBasemodel):
    __tablename__ = 'usuarios'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    nome = Column(
        String(256), 
        nullable=True
    )
    sobrenome = Column(
        String(256),
        nullable=True
    )
    email = Column(
        String(256),
        index=True,
        nullable=False,
        unique=True
    )
    senha = Column(
        String(256),
        nullable=False
    )
    eh_admin = Column(
        Boolean,
        default=False
    )
    tipo_usuario = Column(
        String(256),
        nullable=True,
        default='usuario'
    )
    
  

