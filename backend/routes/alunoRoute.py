from fastapi import APIRouter, HTTPException, status
from DB import db
from entidades.Aluno import Aluno
from controllers import alunosControllers

alunoRoutes = APIRouter()
# database = db.Database()

@alunoRoutes.get("/alunos")
def getAlunoData():
    return alunosControllers.getAllAlunos()

@alunoRoutes.post("/alunos", status_code= status.HTTP_201_CREATED)
def insertAluno(parametro: Aluno):
    try:
        alunosControllers.verificar_campos(parametro)
        alunosControllers.inserirAluno(parametro)
    except ValueError as error:
        raise HTTPException(
            status_code= status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail= f"{error}"
        )

    return