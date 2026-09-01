from enum import Enum

class EquipamentoStatus(str, Enum):
    DISPONIVEL = "Disponivel"
    INDISPONIVEL = "Indisponivel"
    MANUTENCAO = "Manutencao"
    RESERVADO = "Resarvado"