from fastapi import APIRouter
from DB import db

alunoRoutes = APIRouter()
database = db.Database()

@alunoRoutes.get("/alunos")
def getAlunoData():
    return database.getData()

@alunoRoutes.post("/alunos")
def inserAluno(parametro:dict):

    id = parametro.get("id")
    database.insert(id, parametro)