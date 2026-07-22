from fastapi import APIRouter
from DB import db
from entidades import Aluno

alunoRoutes = APIRouter()
database = db.Database

@alunoRoutes.get("/alunos")
def getAlunoData():
    return database.getData()

@alunoRoutes.post("/aluno")
def inserAluno(parametro:dict):
    
    aluno = Aluno()

    aluno.id(parametro.get("id"))
    aluno.nome(parametro.get("nome"))
    aluno.numeroMatricula(parametro.get("numeroMatricula"))
    aluno.curso(parametro.get("curso"))
    aluno.email(parametro.get("email"))
    database.insert(aluno.id, aluno)