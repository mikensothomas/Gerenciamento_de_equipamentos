from entidades.models.categoria_model import CategoriaEquipamento
from sqlmodel import Session, select
from fastapi import HTTPException

def inserirCategoria(categoria: CategoriaEquipamento, db: Session):

    categoria_exixtente = db.exec(
        select(CategoriaEquipamento).where(
            CategoriaEquipamento.categoria_name == categoria.categoria_name
        )
    ).first()
    
    if categoria_exixtente:
        raise HTTPException(
            status_code=400,
            detail="Nome duplicado"
        )
        
    categoria_insert = CategoriaEquipamento.model_validate(categoria)
    db.add(categoria_insert)
    db.commit()
    db.refresh(categoria_insert)
    return categoria_insert