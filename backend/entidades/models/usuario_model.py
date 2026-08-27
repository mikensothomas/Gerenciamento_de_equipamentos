from sqlmodel import SQLModel, Field, Enum as SQLEnum, Column
from datetime import date
from enums.status_usuarios import StatusUsuarios
from enums.perfil_usuarios import PerfilUsuarios

class Usuarios(SQLModel, table = True):
    __tablename__="Usuarios"
    id_usuario: int | None = Field(default=None, primary_key=True)
    cpf: str = Field(max_length=11, unique=True, nullable=True)
    nome: str = Field(max_length=100, nullable=True)
    email: str = Field(max_length=50, nullable=True)
    senha: str = Field(max_length=50, nullable=True)
    status_usuario: StatusUsuarios = Field(
        default=StatusUsuarios.ATIVO,
        sa_column=Column(
            SQLEnum(StatusUsuarios, values_callable=lambda enum: [e.value for e in enum])
        )
    )
    data_cadastro: date = Field(default_factory=date.today)
    perfil: PerfilUsuarios = Field(
        default=PerfilUsuarios.ALUNO,
        sa_column=Column(
            SQLEnum(PerfilUsuarios, values_callable=lambda enum: [e.value for e in enum])
        )
    )