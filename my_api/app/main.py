from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud, security
from .database import engine, SessionLocal, Base

# Inicialização do FastAPI
app = FastAPI()

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Definição de usuários fictícios para o banco de dados
fake_db = [
    models.User(email="user1@example.com", name="User 1", hashed_password=security.get_password_hash("password1"), user_type="user"),
    models.User(email="user2@example.com", name="User 2", hashed_password=security.get_password_hash("password2"), user_type="user"),
]

# Função para obter o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para obter o usuário atual com base no token JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = security.decode_token(token)
    user_email = payload.get("sub")
    if user_email is None:
        raise credentials_exception
    user = crud.get_user_by_email(db, user_email)
    if user is None:
        raise credentials_exception
    return user

# Rota para gerar token JWT (login)
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=15)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Rota para listar todos os usuários (apenas para administradores)
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.user_type != "admin":
        raise HTTPException(status_code=403, detail="You don't have enough permissions")
    return crud.get_all_users(db, skip=skip, limit=limit)

# Rota para criar um novo usuário (apenas para administradores)
@app.post("/users/", response_model=schemas.User)
def create_user(user_in: schemas.UserCreate, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.user_type != "admin":
        raise HTTPException(status_code=403, detail="You don't have enough permissions")
    return crud.create_user(db, user_in)

# Rota para obter um usuário pelo ID (apenas para administradores)
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int = Path(..., title="The ID of the user to retrieve"),
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verificar se o usuário atual é um administrador
    if current_user.user_type != "admin":
        raise HTTPException(status_code=403, detail="You don't have enough permissions")
    
    # Obter o usuário pelo ID usando a função do módulo CRUD
    user = crud.get_user_by_id(db, user_id)
    
    # Verificar se o usuário foi encontrado
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# Rota para atualizar as informações de um usuário pelo ID (apenas para administradores)
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verificar se o usuário atual é um administrador
    if current_user.user_type != "admin":
        raise HTTPException(status_code=403, detail="You don't have enough permissions")
    
    # Atualizar o usuário utilizando a função do módulo CRUD
    updated_user = crud.update_user(db, user_id, user_in)
    
    return updated_user

# Rota para excluir um usuário pelo ID (apenas para administradores)
@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(
    user_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verificar se o usuário atual é um administrador
    if current_user.user_type != "admin":
        raise HTTPException(status_code=403, detail="You don't have enough permissions")
    
    # Deletar o usuário utilizando a função do módulo CRUD
    deleted_user = crud.delete_user(db, user_id)
    
    return deleted_user

# Rota para criar um agendamento e um formulário vinculado
@app.post("/schedules/", response_model=schemas.Schedule)
def create_schedule(schedule_in: schemas.ScheduleCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    schedule, form = crud.create_schedule_with_form(db, schedule=schedule_in, user_id=current_user.id)
    return schedule

# Rota para obter todos os agendamentos
@app.get("/schedules/", response_model=List[schemas.Schedule])
def read_schedules(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    schedules = crud.get_schedules(db, skip=skip, limit=limit)
    return schedules

# Rota para obter agendamentos de um usuário específico
@app.get("/users/{user_id}/schedules/", response_model=List[schemas.Schedule])
def read_user_schedules(user_id: int, db: Session = Depends(get_db)):
    schedules = crud.get_schedules_by_user(db, user_id=user_id)
    return schedules

# Rota para obter um agendamento específico pelo ID
@app.get("/schedules/{schedule_id}", response_model=schemas.Schedule)
def read_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = crud.get_schedule(db, schedule_id=schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

# Rota para atualizar um agendamento pelo ID
@app.put("/schedules/{schedule_id}", response_model=schemas.Schedule)
def update_schedule(
    schedule_id: int,
    schedule_in: schemas.ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    schedule = crud.get_schedule(db, schedule_id=schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    if schedule.owner_id != current_user.id and current_user.user_type != "admin":
        raise HTTPException(status_code=403, detail="You don't have permission to update this schedule")
    updated_schedule = crud.update_schedule(db, schedule_id, schedule_in)
    return updated_schedule

# Rota para deletar um agendamento pelo ID
@app.delete("/schedules/{schedule_id}", response_model=schemas.Schedule)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = crud.delete_schedule(db, schedule_id=schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

# Rota para obter todos os formulários
@app.get("/forms/", response_model=List[schemas.Form])
def read_forms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    forms = crud.get_forms(db, skip=skip, limit=limit)
    return forms

# Rota para obter um formulário específico pelo ID
@app.get("/forms/{form_id}", response_model=schemas.Form)
def read_form(form_id: int, db: Session = Depends(get_db)):
    form = crud.get_form(db, form_id=form_id)
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    return form

# Rota para atualizar um formulário pelo ID
@app.put("/forms/{form_id}", response_model=schemas.Form)
def update_form(form_id: int, form: schemas.FormUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_form = crud.get_form(db, form_id=form_id)
    if db_form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    schedule = crud.get_schedule(db, schedule_id=db_form.schedule_id)
    if schedule.owner_id != current_user.id and current_user.user_type != 'admin':
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.update_form(db=db, form_id=form_id, form=form)