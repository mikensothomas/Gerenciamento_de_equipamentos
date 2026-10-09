from sqlmodel import SQLModel, Field, Enum as SQLEnum, Column
from datetime import date
from enums.status_usuarios import StatusUsuarios
from enums.perfil_usuarios import PerfilUsuarios

class Usuarios(SQLModel, table = True):
    __tablename__="usuarios"
    id_usuario: int | None = Field(default=None, primary_key=True)
    cpf: str = Field(max_length=11, unique=True, nullable=False)
    nome: str = Field(max_length=100, nullable=False)
    email: str = Field(max_length=50, nullable=False)
    senha: str = Field(max_length=255, nullable=False)
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


class UsuarioCadastro(SQLModel):
    cpf: str = Field(min_length=11, max_length=11)
    nome: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=50)
    senha: str = Field(min_length=1, max_length=255)
    status_usuario: StatusUsuarios = Field(default=StatusUsuarios.ATIVO)
    perfil: PerfilUsuarios = Field(default=PerfilUsuarios.ALUNO)