from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from urllib.parse import quote_plus

#conexao com o banco de dados
password = "over@002"
quoted_password = quote_plus(password)

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://root:{quoted_password}@localhost/database"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #criação da sessão 

def create_database(): #função para criar o banco de dados 
    Base.metadata.create_all(bind=engine)
