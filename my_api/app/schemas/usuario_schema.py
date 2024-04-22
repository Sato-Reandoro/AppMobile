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
        orm_mode = True

class UsuarioSchemaCreate(UsuarioSchemaBase):
    pass

class UsuarioSchemaUp(UsuarioSchemaBase):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    tipo_usuario: Optional[str]