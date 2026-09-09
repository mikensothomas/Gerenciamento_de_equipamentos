from enum import Enum

class StatusSolicitacao(str, Enum):
    PENDENTE = "Pendente"
    APROVADO = "Aprovado"
    NEGADO = "Negado"
    ATRASO = "Atraso"
    DEVOLVIDO = "Devolvido"