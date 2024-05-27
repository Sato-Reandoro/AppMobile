from fastapi import FastAPI
from sqlalchemy.orm import Session
from core.crud_bd import SessionLocal
from schemas.usuario_schema import UsuarioSchemaBase
from api.v1.endpoints.admin import post_usuario, get_logado, get_usuarios, get_usuario_por_id, get_usuario_por_nome, put_usuario, delete_usuario, login_for_access_token as login
from typing import Generator

app = FastAPI()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.post('/signup', status_code=201, response_model=UsuarioSchemaBase)(post_usuario)
app.get('/logado', response_model=UsuarioSchemaBase)(get_logado)
app.get('/', response_model=list[UsuarioSchemaBase])(get_usuarios)
app.get("/{usuario_id}", response_model=UsuarioSchemaBase, status_code=200)(get_usuario_por_id)
app.get("/nome/{nome}", response_model=UsuarioSchemaBase, status_code=200)(get_usuario_por_nome)
app.put('/atualizar/{usuario_id}', response_model=UsuarioSchemaBase, status_code=202)(put_usuario)
app.delete('/apagar/{usuario_id}', status_code=204)(delete_usuario)
app.post('/login', response_model=UsuarioSchemaBase)(login)

