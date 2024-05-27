from datetime import timedelta
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.database import SessionLocal, get_db
from core.crud_bd import atualizar_dados_usuario, verificar_adm_mesmo, buscar_por_id, buscar_por_nome, criar_novo_usuario, delete_user, verificar_administrador_global, verificar_usuario_logado
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, Response, status, Path
from models.usuarios_model import UsuarioModel
from core.deps import ACCESS_TOKEN_EXPIRE_MINUTES, Token, TokenData, authenticate_user, create_access_token, get_current_user, get_user, verify_password
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate
from starlette.status import HTTP_401_UNAUTHORIZED

app = FastAPI()

@app.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
def post_usuario(usuario: UsuarioSchemaCreate, db: Session = Depends(get_db)):
    try:
        usuario_criado = criar_novo_usuario(db, usuario)
        return usuario_criado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(verificar_usuario_logado)):
    return usuario_logado

@app.get('/', response_model=List[UsuarioSchemaBase])
def get_usuarios(db: Session = Depends(get_db), usuario_logado: UsuarioModel = Depends(get_current_user)):
    verificar_administrador_global(usuario_logado)
    query = select(UsuarioModel)
    result = db.execute(query)
    usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()
    return usuarios

@app.get("/{usuario_id}", response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
def get_usuario_por_id(usuario_id: int, db: Session = Depends(get_db), usuario_logado: UsuarioModel = Depends(get_current_user)):
    verificar_administrador_global(usuario_logado)
    return buscar_por_id(usuario_id, db)
@app.get("/nome/{nome}", response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
def get_usuario_por_nome(nome: str, db: Session = Depends(get_db), usuario_logado: UsuarioModel = Depends(get_current_user)):
    verificar_administrador_global(usuario_logado)  # Verifica se o usuário é um administrador
    return buscar_por_nome(nome, db)


@app.put('/atualizar/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
def put_usuario(usuario_id: int, usuario: UsuarioSchemaCreate, db: Session = Depends(get_db), usuario_logado: UsuarioModel = Depends(get_current_user)):
    verificar_adm_mesmo(usuario_logado, usuario_id)
    verificar_administrador_global(usuario_logado)
    return atualizar_dados_usuario(usuario_id, usuario, db)

@app.delete('/apagar/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db), usuario_logado: UsuarioModel = Depends(get_current_user)):
    verificar_administrador_global(usuario_logado)
    success = delete_user(usuario_id, db)
    if success:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            detail=f'ID do Usuário: {str(usuario_id)}, Não encontrado na Base de Dados!',
            status_code=status.HTTP_404_NOT_FOUND
        )


@app.post("/login", response_model=TokenData)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)  # Ajustado para usar form_data.username, que agora representa o email
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Aqui você deve obter os valores dos campos nome, sobrenome, etc., do usuário
    # Por exemplo, supondo que esses campos estejam disponíveis no objeto user
    nome = user.nome
    sobrenome = user.sobrenome
    email = user.email
    eh_admin = user.eh_admin
    tipo_usuario = user.tipo_usuario

    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "nome": nome,
        "sobrenome": sobrenome,
        "email": email,
        "eh_admin": eh_admin,
        "tipo_usuario": tipo_usuario
        }