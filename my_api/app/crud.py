from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .security import get_password_hash

#User
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        user_type=user.user_type
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_in: schemas.UserUpdate):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = user_in.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return user

def create_schedule(db: Session, schedule_in: schemas.ScheduleCreate):
    db_schedule = models.Schedule(**schedule_in.dict())# Passando o status como uma string
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def get_schedules(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Schedule).offset(skip).limit(limit).all()

def get_schedules_by_user(db: Session, user_id: int):
    return db.query(models.Schedule).filter(models.Schedule.owner_id == user_id).all()

def get_schedule(db: Session, schedule_id: int):
    return db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()

def update_schedule(db: Session, schedule_id: int, schedule_update: schemas.ScheduleUpdate):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    
    if db_schedule is None:
        return None
    
    for key, value in schedule_update.dict(exclude_unset=True).items():
        setattr(db_schedule, key, value)
    
    db.commit()
    db.refresh(db_schedule)
    
    return db_schedule



    
def update_schedule_status(db: Session, schedule_id: int, status: bool):
    """
    Atualiza o status de um agendamento.
    """
    schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not schedule:
        raise Exception("Schedule not found")

    schedule.status = status
    db.commit()
    db.refresh(schedule)
    return schedule

    # Validar e atualizar apenas se o status for um booleano válido
    if schedule.status is not None and isinstance(schedule.status, bool):
        db_schedule.status = schedule.status

    # Atualizar os outros campos se forem fornecidos
    if schedule.name is not None:
        db_schedule.name = schedule.name
    if schedule.condominium is not None:
        db_schedule.condominium = schedule.condominium
    if schedule.date_time is not None:
        db_schedule.date_time = schedule.date_time

    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def delete_schedule(db: Session, schedule_id: int):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    db.delete(db_schedule)
    db.commit()
    return db_schedule

def get_forms(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Form).offset(skip).limit(limit).all()

def get_form(db: Session, form_id: int):
    return db.query(models.Form).filter(models.Form.id == form_id).first()

def update_form(db: Session, form_id: int, form: schemas.FormUpdate):
    db_form = db.query(models.Form).filter(models.Form.id == form_id).first()
    if db_form is None:
        return None
    
    form_data = form.dict(exclude_unset=True)
    for key, value in form_data.items():
        if key in ['data', 'data_condominio'] and value is not None:
            value = str(value)  # Converte para string
        setattr(db_form, key, value)

    db.commit()
    db.refresh(db_form)
    return db_form


from datetime import datetime
from . import models, schemas
from sqlalchemy.orm import Session

def create_form(db: Session, form_data: dict):
    db_form = models.Form(**form_data)
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form

def get_form_by_id(db: Session, form_id: int):
    return db.query(models.Form).filter(models.Form.id == form_id).first()

def update_form(db: Session, form_id: int, form_data: dict):
    db_form = db.query(models.Form).filter(models.Form.id == form_id).first()
    if db_form:
        for key, value in form_data.items():
            setattr(db_form, key, value)
        db.commit()
        db.refresh(db_form)
    return db_form



def delete_form_by_schedule_id(db: Session, schedule_id: int):
    db.query(models.Form).filter(models.Form.schedule_id == schedule_id).delete()
    db.commit()


    