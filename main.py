#importações para execução do código
from fastapi import FastAPI, HTTPException
from database import create_database, SessionLocal
from models import Usuario, NovoUsuario
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

#criação do banco de dados
create_database()

#criação do app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

#criação da rota para o index
@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

#criação da rota para o icone
@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse("static/email.ico")

#criação das rotas 
@app.get("/usuarios/")

#função para listar os usuários
async def listar_usuarios():
    db = SessionLocal() #criação da sessão
    usuarios = db.query(Usuario).all() #query para listar todos os usuários
    if(usuarios): #verificação se a lista de usuários não está vazia
        return usuarios
    raise HTTPException(status_code=404, detail="Lista de usuários vazia!")

@app.post("/usuariosAdd/")

#função para criar um novo usuário
async def criar_usuario(novo_usuario: NovoUsuario):
    db = SessionLocal()
    novo_usuario_db = Usuario(nome=novo_usuario.nome, email=novo_usuario.email)
    db.add(novo_usuario_db) #adiciona o novo usuário
    db.commit()
    db.refresh(novo_usuario_db) #atualiza o banco de dados
    return novo_usuario_db

@app.put("/usuariosAtt/{usuario_id}")

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

