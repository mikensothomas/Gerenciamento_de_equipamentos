from sqlmodel import SQLModel, Field

class CategoriaEquipamento(SQLModel, table = True):
    __tablename__="Categoria_equipamento"
    categoria_id : int | None = Field(default=None, primary_key = True)
    categoria_name : str = Field(max_length = 100, unique = True, nullable = False)