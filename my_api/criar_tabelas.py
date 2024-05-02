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
    



def create_tables(engine):
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    # Substitua 'postgresql://user:password@localhost/AppMobile' pela sua URL de conexão real
    engine = create_engine('postgresql://postgres:2046@localhost:5432/AppMobile')
    create_tables(engine)
    print("Tabelas criadas com sucesso!")
