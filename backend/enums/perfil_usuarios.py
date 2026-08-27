from enum import Enum

class PerfilUsuarios(str, Enum):
    ADMINISTRADOR = "Administrador"
    GESTOR = "Gestor"
    TECNICO = "Tecnico"
    ALUNO = "Aluno"