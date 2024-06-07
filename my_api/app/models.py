from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(String, nullable=False)

    schedules = relationship("Schedule", back_populates="owner")

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    condominium = Column(String, index=True)
    date_time = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Boolean, default=False)

    owner = relationship("User", back_populates="schedules")
    forms = relationship("Form", back_populates="schedule", cascade="all, delete-orphan")

class Form(Base):
    __tablename__ = "forms"

    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("schedules.id"))
    title = Column(String, index=True)
    description = Column(String, index=True)
    projeto = Column(String)
    data = Column(String)  # Deve ser String
    condominio = Column(String)
    cnpj = Column(String)
    sindico = Column(String)
    telefone_sindico = Column(String)
    gerente = Column(String)
    telefone_gerente = Column(String)
    endereco = Column(String)
    email = Column(String)
    cep = Column(String)
    bairro = Column(String)
    data_condominio = Column(String)  # Deve ser String
    unidades = Column(Integer)
    n_elevadores = Column(Integer)
    taxa = Column(Float)
    arrecadacao = Column(Float)
    piscina = Column(Boolean)
    churrasqueira = Column(Boolean)
    academia = Column(Boolean)
    outros = Column(Text, nullable=True)
    quantidade_porteiros = Column(Integer)
    zelador = Column(Boolean)
    faxineiros = Column(Integer)
    possui_alarme = Column(Boolean)
    possui_cerca_cameras = Column(Boolean)
    gerador = Column(Boolean)
    assembleia = Column(Boolean)
    apresentacao = Column(Boolean)
    tipo_condominio = Column(String)
    acesso_pedestre = Column(Boolean)
    acesso_veicular = Column(Boolean)
    eclusa = Column(Boolean)
    despesa_atual_portaria = Column(Float)
    tipo_portaria = Column(String)
    situacao = Column(String)
    valor_link_instalacao = Column(Float)
    info_adicional = Column(Text, nullable=True)
    como_conheceu_a_porter = Column(String)

    schedule = relationship("Schedule", back_populates="forms")
