from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, text
from typing import Optional
from datetime import datetime


class Perfil(SQLModel, table=True):
    __tablename__ = "perfil"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    nome: str = Field(
        max_length=100,
        unique=True
    )

    descricao: str = Field(
        max_length=255
    )

    status: str = Field(
        default="ativo",
        max_length=7
    )

    data_criacao: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime,
            server_default=text("CURRENT_TIMESTAMP")
        )
    )