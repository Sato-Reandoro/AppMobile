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
    status = Column(String, index=True, default="pending")  # Definindo o campo status como uma strin

     # Adicione a coluna para a chave estrangeira
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Adicione a relação inversa para referenciar o proprietário do agendamento
    owner = relationship("User", back_populates="schedules")
    forms = relationship("Form", back_populates="schedule", cascade="all, delete-orphan")


class Form(Base):
    __tablename__ = "forms"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="")
    data = Column(String, default="")
    condominio = Column(String, default="")
    cnpj = Column(String, default="")
    sindico = Column(String, default="")
    telefone_sindico = Column(String, default="")
    telefone_gerente = Column(String, default="")
    email = Column(String, default="")
    gerente = Column(String, default="")
    cep = Column(String, default="")
    endereco = Column(String, default="")
    bairro = Column(String, default="")
    cidade = Column(String, default="")
    data_condominio = Column(String, default="")
    unidades = Column(String, default="")
    n_elevadores = Column(String, default="")
    taxa = Column(String, default="")
    tipo_condominio = Column(String, default="")
    arrecadacao = Column(String, default="")
    academia = Column(String, default="")
    piscina = Column(String, default="")
    churrasqueira = Column(String, default="")
    outros = Column(String, default="")
    quantidade_porteiros = Column(String, default="")
    gerente_zelador = Column(String, default="")
    faxineiros = Column(String, default="")
    possui_cerca_cameras = Column(String, default="")
    possui_alarme = Column(String, default="")
    gerador = Column(String, default="")
    assembleia = Column(String, default="")
    apresentacao = Column(String, default="")
    acesso_pedestre = Column(String, default="")
    acesso_veicular = Column(String, default="")
    eclusa = Column(String, default="")
    despesa_atual_portaria = Column(String, default="")
    valor_link_instalacao = Column(String, default="")
    tipo_portaria = Column(String, default="")
    situacao = Column(String, default="")
    info_adicional = Column(String, default="")
    como_conheceu_a_porter = Column(String, default="")

    schedule_id = Column(Integer, ForeignKey("schedules.id"))

    schedule = relationship("Schedule", back_populates="forms")