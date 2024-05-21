from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    senha: str
    tipo_usuario: str

class Config:
        from_attributes = True

class UsuarioSchemaCreate(UsuarioSchemaBase):
    eh_admin: Optional[bool] = None  # Indica se o usuário é administrador
    tipo_usuario: Optional[str] = None  # Tipo de usuário (por exemplo, 'admin' ou 'funcionario')

class UsuarioSchemaUp(UsuarioSchemaBase):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    tipo_usuario: Optional[str]
