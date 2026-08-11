from entidades.Aluno import Aluno
from DB.db import Database

database = Database()

def verificar_campos(aluno: Aluno):
    if not aluno.nome:
        raise ValueError("Nome informado inválido")

    if "@" not in aluno.email:
        raise ValueError("Email inválido")

    if not aluno.curso:
        raise ValueError("Curso informado inválido")
    
    if not aluno.numero_matricula:
            raise ValueError("Matricula informada inválida")

def inserirAluno(aluno: Aluno):
     id = next(database.next_index())
     database.insert(id, aluno)

def getAllAlunos():
     return database.getData()