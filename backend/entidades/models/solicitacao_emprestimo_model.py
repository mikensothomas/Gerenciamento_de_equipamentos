from sqlmodel import SQLModel, Field, Enum as SQLEnum, Column
from enums.solicitacaoEmprestimoEnum import StatusSolicitacao
from datetime import datetime
from sqlalchemy import DateTime, FetchedValue

class SolicitacaoEmprestimo(SQLModel, table = True):
    __tablename__="solicitacao_emprestimo"
    id_solicitacao_emprestimo : int | None = Field(default=None, primary_key = True)
    status_solicitacao : StatusSolicitacao = Field(
        default=StatusSolicitacao.PENDENTE,
        sa_column=Column(
            SQLEnum(StatusSolicitacao, values_callable=lambda enum: [e.value for e in enum])
        )
    )
    data_solicitacao : datetime = Field(default_factory=datetime.now)
    data_aprovacao: datetime | None = Field(default=None)
    tempo_estimado_devolucao: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime,
            FetchedValue(),
        ),
    )
    equipamento_id : int = Field(foreign_key="equipamento.equipamento_id")
    usuario_id : int = Field(foreign_key="usuarios.id_usuario")
    id_aprovador : int | None = Field(foreign_key="usuarios.id_usuario")