from sqlmodel import SQLModel, Field, Relationship, Enum as SQLEnum, Column
from typing import TYPE_CHECKING
from enums.equipamento import EquipamentoStatus

if TYPE_CHECKING:
    from entidades.models.categoria_model import CategoriaEquipamento


class EquipamentoBase(SQLModel):
    nome: str = Field(max_length=100)
    patrimonio: str = Field(min_length=3, max_length=10)
    marca: str = Field(min_length=3, max_length=100)
    modelo: str = Field(min_length=3, max_length=50)
    descricao: str = Field(max_length=255)

    status_equipamento: EquipamentoStatus = Field(default=EquipamentoStatus.DISPONIVEL, sa_column=Column(
            SQLEnum(
                EquipamentoStatus,
                values_callable=lambda enum: [item.value for item in enum]
            )
        )
    )

    equipamento_categoria_id: int = Field(
        foreign_key="Categoria_equipamento.categoria_id"
    )


class Equipamento(EquipamentoBase, table=True):
    __tablename__ = "Equipamento"

    equipamento_id: int | None = Field(
        default=None,
        primary_key=True
    )

    equipamento_categoria: "CategoriaEquipamento" = Relationship(
        back_populates="equipamentos"
    )


class EquipamentoResponse(SQLModel):
    equipamento_id: int
    nome: str
    patrimonio: str
    marca: str
    modelo: str
    descricao: str
    status_equipamento: EquipamentoStatus
    equipamento_categoria_id: int