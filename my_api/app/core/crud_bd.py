from core.database import get_db
from core.deps import get_current_user
from core.security import gerar_hash_senha
from fastapi import HTTPException
from fastapi import Depends, HTTPException, status
from models.usuarios_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate
from sqlalchemy.orm import Session
from sqlalchemy import select
from core.configs import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from typing import List
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext


settings.DB_URL = "postgresql://postgres:2046@localhost:5432/AppMobile"



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("mysecretpassword")


# Criando o motor de banco de dados síncrono
engine = create_engine(settings.DB_URL)

# Definindo a fábrica de sessões síncronas
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)

Base = declarative_base()

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def verificar_email_em_uso(email: str, db: Session) -> bool:
    query = select(UsuarioModel).filter(UsuarioModel.email == email)
    result = db.execute(query)
    usuario_existente: UsuarioModel = result.scalar_one_or_none()
    return usuario_existente is not None

def definir_tipo_usuario(tipo_usuario: str) -> tuple[bool, str]:
    if tipo_usuario == 'admin':
        return True, 'admin'
    elif tipo_usuario == 'funcionario':
        return False, 'funcionario'
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de usuário inválido.")

def criar_novo_usuario(db: Session, usuario: UsuarioSchemaCreate):
    novo_usuario = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=pwd_context.hash(usuario.senha),  # Hash da senha antes de salvar
        eh_admin=usuario.eh_admin,
        tipo_usuario=usuario.tipo_usuario
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

#verificação global de adm
def verificar_administrador_global(usuario_logado: UsuarioModel):
    if not usuario_logado.eh_admin:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para acessar esta rota."
        )

#usuario logado 
def verificar_usuario_logado(db: Session = Depends(get_db)):
    usuario_logado = get_current_user(db)
    if not usuario_logado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não logado"
        )
    elif not usuario_logado.eh_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Somente administradores podem acessar esta rota."
        )
    return usuario_logado

#get users
def obter_usuarios(db: Session = Depends(get_db)):
    usuario_logado = get_current_user(db)
    verificar_administrador_global(usuario_logado)  # Verifica se o usuário é um administrador
    usuarios = db.query(UsuarioModel).all()
    return usuarios

#get users por id 
def buscar_por_id(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).get(usuario_id)
    if usuario:
        return usuario
    else:
        raise HTTPException(
            detail=f'ID do Usuário: {str(usuario_id)} não encontrado na Base de Dados!',
            status_code=status.HTTP_404_NOT_FOUND
        )
   
def buscar_por_nome(nome: str, db: Session = Depends(get_session)):
    query = select(UsuarioModel).filter(UsuarioModel.nome == nome)
    result = db.execute(query)
    usuario: UsuarioSchemaBase = result.scalar_one_or_none()
    if usuario:
        return usuario
    else:
        raise HTTPException(
            detail=f'Nome do Usuário: {nome} não encontrado na Base de Dados!',
            status_code=status.HTTP_404_NOT_FOUND
        )


#put users
def verificar_adm_mesmo(usuario_logado: UsuarioModel, usuario_id: int):
    if usuario_logado.id!= usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Um administrador só pode atualizar sua própria conta."
        )
    
def atualizar_dados_usuario(usuario_id, usuario_atualizado, db: Session):
    usuario_antigo = db.query(UsuarioModel).get(usuario_id)

    if usuario_antigo:
        if usuario_atualizado.nome:
            usuario_antigo.nome = usuario_atualizado.nome
        if usuario_atualizado.sobrenome:
            usuario_antigo.sobrenome = usuario_atualizado.sobrenome
        if usuario_atualizado.email:
            usuario_antigo.email = usuario_atualizado.email
        if usuario_atualizado.eh_admin:
            usuario_antigo.eh_admin = usuario_atualizado.eh_admin
        if usuario_atualizado.senha:
            usuario_antigo.senha = gerar_hash_senha(usuario_atualizado.senha)

        db.commit()
        return usuario_antigo
    else:
        raise HTTPException(
            detail=f'ID do Usuário: {str(usuario_id)}, Não encontrado na Base de Dados!',
            status_code=status.HTTP_404_NOT_FOUND
        )

#delete users
def delete_user(usuario_id: int, db: Session = Depends(get_db)):
    usuario_del = db.query(UsuarioModel).get(usuario_id)
    if usuario_del:
        db.delete(usuario_del)
        db.commit()
        return True
    else:
        return False
