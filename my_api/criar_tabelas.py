from sqlalchemy import Boolean, create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    sobrenome = Column(String)
    email = Column(String, unique=True)
    senha = Column(String)
    eh_admin = Column(Boolean, default=False)
    

class Agendamento(Base):
    __tablename__ = 'agendamento'
    id = Column(Integer, primary_key=True)
    data_hora = Column(DateTime)
    funcionario_id = Column(Integer, ForeignKey('funcionario.id'))

class Formulario(Base):
    __tablename__ = 'formulario'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    descricao = Column(String)
    funcionario_id = Column(Integer, ForeignKey('funcionario.id'))


def create_tables(engine):
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    # Substitua 'postgresql://user:password@localhost/AppMobile' pela sua URL de conexão real
    engine = create_engine('postgresql://postgres:2046@localhost:5432/AppMobile')
    create_tables(engine)
    print("Tabelas criadas com sucesso!")
