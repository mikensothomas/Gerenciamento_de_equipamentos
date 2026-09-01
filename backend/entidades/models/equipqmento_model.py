from sqlmodel import SQLModel, Field, Enum as Relationship
from categoria_model import CategoriaEquipamento
from enums.equipamento import EquipamentoStatus
class EquipqmentoBase(SQLModel):
    nome : str = Field(max_length=100)
    patrimonio : str = Field(min_length=3, max_length=10)
    marca : str = Field(min_length=3, max_length=100)
    modelo : str = Field(min_length=3, max_length=50)
    descricao : str = Field(max_length = 255)
    status_equipamento : EquipamentoStatus = Field(default = EquipamentoStatus.DISPONIVEL)
    equipamento_categoria_id : int = Field(foreign_key="categoria_id")
    

class Equipamento(EquipqmentoBase, table = True):
    __tablename__="Equipamento"
    equipamento_id : int | None = Field(primary_key=True)
    equipamento_categoria: CategoriaEquipamento = Relationship(back_populates="equipamentos")