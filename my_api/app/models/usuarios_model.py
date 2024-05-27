from sqlalchemy import Boolean, Column, Integer, String
from core.database import Base

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    sobrenome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    eh_admin = Column(Boolean, default=False)
    tipo_usuario = Column(String, index=True)
