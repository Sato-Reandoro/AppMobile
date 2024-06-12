from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str
    user_type: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    user_type: str

    class Config:
        orm_mode = True

class ScheduleBase(BaseModel):
    name: str
    condominium: str
    date_time: datetime
    status: Optional[str] = "pending"

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int

    class Config:
        orm_mode = True

class FormBase(BaseModel):
    title: Optional[str] = ""
    data: Optional[str] = ""
    condominio: Optional[str] = ""
    cnpj: Optional[str] = ""
    sindico: Optional[str] = ""
    telefone_sindico: Optional[str] = ""
    telefone_gerente: Optional[str] = ""
    email: Optional[str] = ""
    gerente: Optional[str] = ""
    cep: Optional[str] = ""
    endereco: Optional[str] = ""
    bairro: Optional[str] = ""
    cidade: Optional[str] = ""
    data_condominio: Optional[str] = ""
    unidades: Optional[str] = ""
    n_elevadores: Optional[str] = ""
    taxa: Optional[str] = ""
    tipo_condominio: Optional[str] = ""
    arrecadacao: Optional[str] = ""
    academia: Optional[str] = ""
    piscina: Optional[str] = ""
    churrasqueira: Optional[str] = ""
    outros: Optional[str] = ""
    quantidade_porteiros: Optional[str] = ""
    gerente_zelador: Optional[str] = ""
    faxineiros: Optional[str] = ""
    possui_cerca_cameras: Optional[str] = ""
    possui_alarme: Optional[str] = ""
    gerador: Optional[str] = ""
    assembleia: Optional[str] = ""
    apresentacao: Optional[str] = ""
    acesso_pedestre: Optional[str] = ""
    acesso_veicular: Optional[str] = ""
    eclusa: Optional[str] = ""
    despesa_atual_portaria: Optional[str] = ""
    valor_link_instalacao: Optional[str] = ""
    tipo_portaria: Optional[str] = ""
    situacao: Optional[str] = ""
    info_adicional: Optional[str] = ""
    como_conheceu_a_porter: Optional[str] = ""

class FormCreate(FormBase):
    pass

class FormUpdate(FormBase):
    pass

class Form(FormBase):
    id: int

    class Config:
        orm_mode = True