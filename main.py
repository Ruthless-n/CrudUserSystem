#importações para execução do código

from fastapi import FastAPI, HTTPException
from database import create_database, SessionLocal
from models import Usuario

#criação do banco de dados
create_database()

#criação do app
app = FastAPI()

#criação das rotas 
@app.get("/usuarios/")
#função para listar os usuários
async def listar_usuarios():
    db = SessionLocal() #criação da sessão
    usuarios = db.query(Usuario).all() #query para listar todos os usuários
    if(usuarios): #verificação se a lista de usuários não está vazia
        return usuarios
    raise HTTPException(status_code=404, detail="Lista de usuários vazia!")

@app.post("/usuarios/")
#função para criar um novo usuário
async def criar_usuario(nome: str, email: str):
    db = SessionLocal()
    novo_usuario = Usuario(nome=nome, email=email)
    db.add(novo_usuario) #adiciona o novo usuário
    db.commit()
    db.refresh(novo_usuario) #atualiza o banco de dados
    return novo_usuario

@app.put("/usuarios/{usuario_id}")
#função para atualizar um usuário
async def atualizar_usuario(usuario_id: int, nome: str, email: str):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first() #query para buscar o usuário pelo id
    if usuario: #verificação se o usuário existe
        usuario.nome = nome
        usuario.email = email
        db.commit()
        db.refresh(usuario)
        return usuario
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.delete("/usuarios/{usuario_id}")
#função para deletar um usuário
async def deletar_usuario(usuario_id: int):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        db.delete(usuario) #deleta o usuário
        db.commit()
        return {"mensagem": "Usuário deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

