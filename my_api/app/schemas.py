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
    name: Optional[str]
    condominium: Optional[str]
    date_time: Optional[datetime]
    status: Optional[bool] = False

class ScheduleCreate(ScheduleBase):
    name: str
    condominium: str
    date_time: datetime

class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    condominium: Optional[str] = None
    date_time: Optional[datetime] = None
    status: Optional[bool] = None

class Schedule(ScheduleBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class FormBase(BaseModel):
    title: Optional[str]
    description: Optional[str]
    projeto: Optional[str] = None
    data: Optional[str] = None
    condominio: Optional[str] = None
    cnpj: Optional[str] = None
    sindico: Optional[str] = None
    telefone_sindico: Optional[str] = None
    gerente: Optional[str] = None
    telefone_gerente: Optional[str] = None
    endereco: Optional[str] = None
    email: Optional[str] = None
    cep: Optional[str] = None
    bairro: Optional[str] = None
    data_condominio: Optional[str] = None
    unidades: Optional[int] = None
    n_elevadores: Optional[int] = None
    taxa: Optional[float] = None
    arrecadacao: Optional[float] = None
    piscina: Optional[bool] = None
    churrasqueira: Optional[bool] = None
    academia: Optional[bool] = None
    outros: Optional[str] = None
    quantidade_porteiros: Optional[int] = None
    zelador: Optional[bool] = None
    faxineiros: Optional[int] = None
    possui_alarme: Optional[bool] = None
    possui_cerca_cameras: Optional[bool] = None
    gerador: Optional[bool] = None
    assembleia: Optional[bool] = None
    apresentacao: Optional[bool] = None
    tipo_condominio: Optional[str] = None
    acesso_pedestre: Optional[bool] = None
    acesso_veicular: Optional[bool] = None
    eclusa: Optional[bool] = None
    despesa_atual_portaria: Optional[float] = None
    tipo_portaria: Optional[str] = None
    situacao: Optional[str] = None
    valor_link_instalacao: Optional[float] = None
    info_adicional: Optional[str] = None
    como_conheceu_a_porter: Optional[str] = None

    class Config:
        orm_mode = True

class FormCreate(FormBase):
    title: str
    description: str

class Form(FormBase):
    id: int
    schedule_id: int

    class Config:
        orm_mode = True

class FormUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    projeto: Optional[str]
    data: Optional[str]  # String opcional para garantir que possa ser convertida
    condominio: Optional[str]
    cnpj: Optional[str]
    sindico: Optional[str]
    telefone_sindico: Optional[str]
    gerente: Optional[str]
    telefone_gerente: Optional[str]
    endereco: Optional[str]
    email: Optional[str]
    cep: Optional[str]
    bairro: Optional[str]
    data_condominio: Optional[str]  # String opcional para garantir que possa ser convertida
    unidades: Optional[int]
    n_elevadores: Optional[int]
    taxa: Optional[float]
    arrecadacao: Optional[float]
    piscina: Optional[bool]
    churrasqueira: Optional[bool]
    academia: Optional[bool]
    outros: Optional[str]
    quantidade_porteiros: Optional[int]
    zelador: Optional[bool]
    faxineiros: Optional[int]
    possui_alarme: Optional[bool]
    possui_cerca_cameras: Optional[bool]
    gerador: Optional[bool]
    assembleia: Optional[bool]
    apresentacao: Optional[bool]
    tipo_condominio: Optional[str]
    acesso_pedestre: Optional[bool]
    acesso_veicular: Optional[bool]
    eclusa: Optional[bool]
    despesa_atual_portaria: Optional[float]
    tipo_portaria: Optional[str]
    situacao: Optional[str]
    valor_link_instalacao: Optional[float]
    info_adicional: Optional[str]
    como_conheceu_a_porter: Optional[str]

    class Config:
        orm_mode = True