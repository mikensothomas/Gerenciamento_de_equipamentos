from dataclasses import dataclass

@dataclass
class Aluno:
    id: int
    nome: str
    numero_matricula: str
    curso: str
    email: str

@property
def dominio_email(self):
    return str.split(self.email, "@")[1]