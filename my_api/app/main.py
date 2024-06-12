from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, Path, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud, security
from .database import engine, SessionLocal, Base
from fastapi.middleware.cors import CORSMiddleware

# Inicialização do FastAPI
app = FastAPI()

# Configuração do CORS para permitir todos os tipos de origens, métodos e cabeçalhos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos os domínios. Você pode restringir a origem conforme necessário.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.).
    allow_headers=["*"],  # Permite todos os cabeçalhos.
)

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

# Rota para obter as informações do usuário autenticado
@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


# Rota para listar todos os usuários
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_users(db, skip=skip, limit=limit)

# Rota para criar um novo usuário
@app.post("/users/", response_model=schemas.User)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user_in)

# Rota para obter um usuário pelo ID
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int = Path(..., title="The ID of the user to retrieve"),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Rota para atualizar as informações de um usuário pelo ID
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    updated_user = crud.update_user(db, user_id, user_in)
    return updated_user

# Rota para excluir um usuário pelo ID
@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    deleted_user = crud.delete_user(db, user_id)
    return deleted_user


# Função para criar um formulário vinculado a um agendamento
def create_linked_form(schedule_id: int, db: Session):
    form_data = {
        "title": "",
        "data": "",
        "condominio": "",
        "cnpj": "",
        "sindico": "",
        "telefone_sindico": "",
        "telefone_gerente": "",
        "email": "",
        "gerente": "",
        "cep": "",
        "endereco": "",
        "bairro": "",
        "cidade": "",
        "data_condominio": "",
        "unidades": "",
        "n_elevadores": "",
        "taxa": "",
        "tipo_condominio": "",
        "arrecadacao": "",
        "academia": "",
        "piscina": "",
        "churrasqueira": "",
        "outros": "",
        "quantidade_porteiros": "",
        "gerente_zelador": "",
        "faxineiros": "",
        "possui_cerca_cameras": "",
        "possui_alarme": "",
        "gerador": "",
        "assembleia": "",
        "apresentacao": "",
        "acesso_pedestre": "",
        "acesso_veicular": "",
        "eclusa": "",
        "despesa_atual_portaria": "",
        "valor_link_instalacao": "",
        "tipo_portaria": "",
        "situacao": "",
        "info_adicional": "",
        "como_conheceu_a_porter": "",
        "schedule_id": schedule_id
    }
    return crud.create_form(db, form_data=form_data)

# Rota para criar um agendamento e um formulário vinculado
@app.post("/schedules/", response_model=schemas.Schedule)
def create_schedule(schedule_in: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    # Criar o agendamento
    schedule = crud.create_schedule(db, schedule_in=schedule_in)
    
    # Criar um formulário vinculado ao agendamento com todos os campos preenchidos como strings vazias
    create_linked_form(schedule_id=schedule.id, db=db)
    
    return schedule



@app.get("/schedules/", response_model=List[schemas.Schedule])
def read_schedules(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    schedules = crud.get_schedules(db, skip=skip, limit=limit)
    # Convertendo a data e hora para string
    for schedule in schedules:
        schedule.date_time = schedule.date_time.strftime("%Y-%m-%d %H:%M:%S")
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

@app.put("/schedules/{schedule_id}", response_model=schemas.Schedule)
def update_schedule(
    schedule_id: int,
    schedule: schemas.ScheduleUpdate,  # Assumindo que você tenha um esquema de atualização
    db: Session = Depends(get_db)
):
    db_schedule = crud.get_schedule(db, schedule_id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    updated_schedule = crud.update_schedule(db, schedule_id, schedule)
    
    if updated_schedule is None:
        raise HTTPException(status_code=404, detail="Failed to update schedule")
    
    updated_schedule.date_time = updated_schedule.date_time.strftime("%Y-%m-%d %H:%M:%S")
    
    return updated_schedule



@app.put("/schedules/complete/{schedule_id}")
def mark_schedule_as_completed(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    schedule = crud.get_schedule(db, schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # Atualiza o status do agendamento para True
    crud.update_schedule_status(db, schedule_id, status=True)
    
    # Retornar uma resposta vazia com código de status 204
    return Response(status_code=204)


@app.put("/schedules/pending/{schedule_id}")
def mark_schedule_as_pending(schedule_id: int, db: Session = Depends(get_db)):
    schedule = crud.get_schedule(db, schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # Atualiza o status do agendamento para False (pendente)
    crud.update_schedule_status(db, schedule_id, status=False)
    
    # Retornar uma resposta vazia com código de status 204
    return Response(status_code=204)

# Rota para deletar um agendamento pelo ID

@app.delete("/schedules/{schedule_id}", response_model=schemas.Schedule)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_schedule = crud.get_schedule(db, schedule_id=schedule_id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")

    # Exclua o agendamento
    deleted_schedule = crud.delete_schedule(db, schedule_id=schedule_id)

    # Exclua o formulário associado
    deleted_form = crud.delete_form_by_schedule_id(db, schedule_id=schedule_id)

    # Converter datetime para string
    deleted_schedule.date_time = deleted_schedule.date_time.strftime("%Y-%m-%d %H:%M:%S")

    return deleted_schedule

# Rota para obter um formulário por ID
@app.get("/forms/{form_id}", response_model=schemas.Form)
def read_form(form_id: int, db: Session = Depends(get_db)):
    db_form = crud.get_form_by_id(db, form_id=form_id)
    if db_form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    return db_form

# Rota para atualizar um formulário por ID
@app.put("/forms/{form_id}", response_model=schemas.Form)
def update_form(form_id: int, form_in: schemas.FormUpdate, db: Session = Depends(get_db)):
    db_form = crud.get_form_by_id(db, form_id=form_id)
    if db_form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    db_form = crud.update_form(db, form_id=form_id, form_data=form_in.dict())
    return db_form