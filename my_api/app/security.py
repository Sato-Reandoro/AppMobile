from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from . import schemas
from .models import User
from sqlalchemy.orm import Session
from . import models

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para verificar se a senha fornecida é correta
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Função para gerar um hash da senha
def get_password_hash(password):
    return pwd_context.hash(password)

# Função para autenticar o usuário
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.email == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


# Função para obter o usuário do banco de dados
def get_user(fake_db: list[User], email: str):
    for user in fake_db:
        if user.email == email:
            return user

# Função para gerar token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para decodificar token JWT
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
