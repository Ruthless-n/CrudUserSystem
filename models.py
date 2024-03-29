from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

#criação da classe Usuario
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    email = Column(String(100), unique=True)

class NovoUsuario(BaseModel):
    nome: str
    email: str

