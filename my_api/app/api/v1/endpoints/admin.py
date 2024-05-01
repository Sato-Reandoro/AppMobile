# /api/v1/endpoints/admin.py
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select

from sqlite3 import IntegrityError
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.usuarios_model import UsuarioModel
from core.deps import get_session, get_current_user
from schemas.usuario_schema import (
    UsuarioSchemaBase,
    UsuarioSchemaCreate,
    UsuarioSchemaUp
)
from core.auth import autentica, criar_token_acesso, gerar_hash_senha

router = APIRouter()

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    # Verificando se o email já está em uso
    query = select(UsuarioModel).filter(UsuarioModel.email == usuario.email)
    result = await db.execute(query)
    usuario_existente: UsuarioModel = result.scalars().unique().one_or_none()

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso."
        )

    # Definindo automaticamente eh_admin com base no tipo_usuario
    if usuario.tipo_usuario == 'admin':
        eh_admin = True
        tipo_usuario = 'admin'
    elif usuario.tipo_usuario == 'funcionario':
        eh_admin = False
        tipo_usuario = 'funcionario'
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de usuário inválido. Use 'admin' para administrador ou 'funcionario' para funcionário."
        )

    novo_usuario = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
        eh_admin=eh_admin,
        tipo_usuario=tipo_usuario
    )

    try:
        db.add(novo_usuario)
        await db.commit()
        await db.refresh(novo_usuario)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar o usuário. Verifique os dados fornecidos."
        )

    return novo_usuario

@router.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    # Verificando se o usuário é um administrador
    if not usuario_logado.eh_admin and usuario_logado.tipo_usuario!= 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Somente administradores podem acessar esta rota."
        )
    return usuario_logado


@router.get('/', response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    usuario_logado = Depends(get_current_user)
    # Verificando se o usuário é um administrador
    if not usuario_logado.eh_admin and usuario_logado.tipo_usuario!= 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Somente administradores podem acessar esta rota."
        )
    # Implementação do get para administradores
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()
        return usuarios

@router.get('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    usuario_logado = Depends(get_current_user)
    # Verificando se o usuário é um administrador
    if not usuario_logado.eh_admin and usuario_logado.tipo_usuario!= 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Somente administradores podem acessar esta rota."
        )
    # Implementação do get por ID para administradores
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaBase = result.scalars().unique().one_or_none()
        if usuario:
            return usuario
        else:
            raise HTTPException(
                detail=f'ID do Usuário: {str(usuario_id)}, Não encontrado na Base de Dados!',
                status_code=status.HTTP_404_NOT_FOUND
            )

@router.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUp, db: AsyncSession = Depends(get_session)):
    usuario_logado = Depends(get_current_user)
    # Verificando se o usuário é um administrador
    if not usuario_logado.eh_admin and usuario_logado.tipo_usuario!= 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Somente administradores podem acessar esta rota."
        )
    # Implementação do put para administradores
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalars().unique().one_or_none()
        if usuario_up:
            if usuario.nome:
                usuario_up.nome = usuario.nome
            if usuario.sobrenome:
                usuario_up.sobrenome = usuario.sobrenome
            if usuario.email:
                usuario_up.email = usuario.email
            if usuario.eh_admin:
                usuario_up.eh_admin = usuario.eh_admin
            if usuario.senha:
                usuario_up.senha = gerar_hash_senha(usuario.senha)
            await session.commit()
            return usuario_up
        else:
            raise HTTPException(
                detail=f'ID do Usuário: {str(usuario_id)}, Não encontrado na Base de Dados!',
                status_code=status.HTTP_404_NOT_FOUND
            )

@router.delete('/apagar/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    usuario_logado = Depends(get_current_user)
    # Verificando se o usuário é um administrador
    if not usuario_logado.eh_admin and usuario_logado.tipo_usuario!= 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Somente administradores podem acessar esta rota."
        )
    # Implementação do delete para administradores
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del: UsuarioSchemaBase = result.scalars().unique().one_or_none()
        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                detail=f'ID do Usuário: {str(usuario_id)}, Não encontrado na Base de Dados!',
                status_code=status.HTTP_404_NOT_FOUND
            )

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.usuarios_model import UsuarioModel
from core.deps import get_session
from schemas.usuario_schema import UsuarioSchemaBase
from core.auth import autentica, criar_token_acesso

router = APIRouter()

@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autentica(email=form_data.username, senha=form_data.password, db=db) # Autenticando usuário

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Dados de acesso incorretos!'
        )

    return {"acess_token": criar_token_acesso(sub=usuario.id), "token_type": "bearer"}