from entidades.models.categoria_model import CategoriaEquipamento
from sqlmodel import Session

def inserirCategoria(categoria: CategoriaEquipamento, db: Session):
    categoria_insert = CategoriaEquipamento.model_validate(categoria)
    db.add(categoria_insert)
    db.commit()
    db.refresh(categoria_insert)
    return categoria_insert