# /api/v1/endpoints/admin.py
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.crud_bd import SessionLocal, atualizar_dados_usuario, buscar_por_id, buscar_por_nome, criar_novo_usuario, delete_user, obter_usuarios, verificar_adm_mesmo, verificar_administrador_global, verificar_usuario_logado
from fastapi.security import OAuth2PasswordRequestForm



from typing import List
from fastapi import Depends, FastAPI, HTTPException, Response, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from models.usuarios_model import UsuarioModel
from core.deps import get_session, get_current_user
from schemas.usuario_schema import (
    UsuarioSchemaBase,
    UsuarioSchemaCreate,
    UsuarioSchemaUp
)
from core.auth import autentica, criar_token_acesso, gerar_hash_senha

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(usuario: UsuarioSchemaCreate, db: Session = Depends(get_db)):
    criar_novo_usuario(db, usuario)
    return {"message": "Usuário criado com sucesso.", "tipo_usuario": usuario.tipo_usuario}

@app.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(verificar_usuario_logado)):
    return usuario_logado

@app.get('/', response_model=List[UsuarioSchemaBase])
async def get_usuarios():
    return await obter_usuarios()

@app.get("/{usuario_id}", response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def get_usuario_por_id(usuario_id: int = Path(..., title="ID do Usuário", description="ID do usuário para buscar"), db: AsyncSession = Depends(get_session)):
    usuario_logado = Depends(get_current_user)
    verificar_administrador_global(usuario_logado)  # Verifica se o usuário é um administrador
    return await buscar_por_id(usuario_id, db)

@app.get("/nome/{nome}", response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def get_usuario_por_nome(nome: str = Path(..., title="Nome do Usuário", description="Nome do usuário para buscar"), db: AsyncSession = Depends(get_session)):
    usuario_logado = Depends(get_current_user)
    verificar_administrador_global(usuario_logado)  # Verifica se o usuário é um administrador
    return await buscar_por_nome(nome, db)

@app.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUp, db: AsyncSession = Depends(get_session)):
    usuario_logado = Depends(get_current_user)
    verificar_administrador_global(usuario_logado)  # Verifica se o usuário é um administrador
    verificar_adm_mesmo(usuario_logado, usuario_id)  # Verifica se o administrador é o mesmo que está tentando atualizar
    return await atualizar_dados_usuario(usuario_id, usuario, db)


@app.delete('/apagar/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    usuario_logado = Depends(get_current_user)
    verificar_administrador_global(usuario_logado)  # Verifica se o usuário é um administrador
    success = await delete_user(usuario_id, db)
    if success:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            detail=f'ID do Usuário: {str(usuario_id)}, Não encontrado na Base de Dados!',
            status_code=status.HTTP_404_NOT_FOUND
        )




@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autentica(email=form_data.username, senha=form_data.password, db=db) # Autenticando usuário

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Dados de acesso incorretos!'
        )

    return {"acess_token": criar_token_acesso(sub=usuario.id), "token_type": "bearer"}

#atualização de dados