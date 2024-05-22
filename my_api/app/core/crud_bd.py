from core.database import get_db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from core.deps import get_current_user, get_session
from core.security import gerar_hash_senha
from fastapi import HTTPException, status
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from models.usuarios_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate



from typing import List


DATABASE_URL = "postgresql://postgres:2046@localhost:5432/AppMobile"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

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
    # Verifica se o e-mail já está em uso
    if verificar_email_em_uso(usuario.email, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já está em uso.")
    
    # Valida o tipo de usuário
    eh_admin, tipo_usuario = definir_tipo_usuario(usuario.tipo_usuario)
    usuario.eh_admin = eh_admin
    
    try:
        novo_usuario = UsuarioModel(
            nome=usuario.nome,
            sobrenome=usuario.sobrenome,
            email=usuario.email,
            senha=gerar_hash_senha(usuario.senha),
            eh_admin=usuario.eh_admin,
            tipo_usuario=tipo_usuario
        )
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
    except IntegrityError:
        db.rollback()  # Garante que o banco de dados volte ao estado anterior em caso de erro
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar o usuário. Verifique os dados fornecidos.")

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
async def obter_usuarios():
    usuario_logado = Depends(get_current_user)
    verificar_administrador_global(usuario_logado)  # Verifica se o usuário é um administrador
    async with get_session() as db:
        query = select(UsuarioModel)
        result = await db.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()
        return usuarios
    
    #get users por id 
    
async def buscar_por_id(usuario_id: int, db: Session = Depends(get_session)):
     async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaBase = result.scalars().unique().one_or_none()
        if usuario:
            return usuario
        else:
            raise HTTPException(
                detail=f'ID do Usuário: {str(usuario_id)} não encontrado na Base de Dados!',
                status_code=status.HTTP_404_NOT_FOUND
            )

async def buscar_por_nome(nome: str, db: Session = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.nome == nome)
        result = await session.execute(query)
        usuario: UsuarioSchemaBase = result.scalars().unique().one_or_none()
        if usuario:
            return usuario
        else:
            raise HTTPException(
                detail=f'Nome do Usuário: {nome} não encontrado na Base de Dados!',
                status_code=status.HTTP_404_NOT_FOUND
            )
        
#put users
async def verificar_adm_mesmo(usuario_logado: UsuarioModel, usuario_id: int):
    if usuario_logado.id!= usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Um administrador só pode atualizar sua própria conta."
        )

async def atualizar_dados_usuario(usuario_id, usuario_atualizado, db: AsyncSession):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_antigo = result.scalars().unique().one_or_none()

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

            await session.commit()
            return usuario_antigo
        else:
            raise HTTPException(
                detail=f'ID do Usuário: {str(usuario_id)}, Não encontrado na Base de Dados!',
                status_code=status.HTTP_404_NOT_FOUND
            )

            
#delete usrs
async def delete_user(usuario_id: int, db: AsyncSession):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del = result.scalars().unique().one_or_none()
        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()
            return True
        else:
            return False