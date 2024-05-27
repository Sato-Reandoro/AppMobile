from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from core.database import get_db  # Certifique-se de que esta função retorna uma sessão síncrona
from models.usuarios_model import UsuarioModel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("mysecretpassword")


SECRET_KEY = "JZC0124uMY9CZL8W329YMhWOagLf1ZcPKWuqEhc8i9s"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin.py")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    nome: str
    sobrenome: str
    email: str
    senha: str
    eh_admin: bool
    tipo_usuario: str

def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password

access_token_expires = datetime.now(timezone.utc) + timedelta(minutes=30)

def create_access_token(*, data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Função para obter o usuário atual com base no ID do usuário extraído do token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(UsuarioModel).filter(UsuarioModel.username == token_data.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user

#def authenticate_user(db: Session, email: str, password: str):
 #   user = db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
  #  if not user:
   #     return False
    #if pwd_context.verify(password, user.senha):  # Verifica a senha com o hash armazenado
     #   return user
    return False

def get_user(db: Session, email: str) -> Optional[UsuarioModel]:
    return db.query(UsuarioModel).filter(UsuarioModel.email == email).first()



def authenticate_user(email: str, password: str) -> Optional[UsuarioModel]:
    # Obtém o usuário do banco de dados com base no email
    user = get_user(email)
    
    # Verifica se o usuário foi encontrado e se a senha está correta
    if user and user.password == password:
        return user
    
    # Retorna None se o usuário não for encontrado ou se a senha estiver incorreta
    return None
