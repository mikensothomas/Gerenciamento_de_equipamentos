from entidades.models.equipamento_model import Equipamento
from sqlmodel import Session, select
from fastapi import HTTPException


def deletarEquipamento(id: int, db: Session):
    equipamento = db.exec(
        select(Equipamento).where(
            Equipamento.equipamento_id == id
        )
    ).first()

    if not equipamento:
        raise HTTPException(
            status_code=404,
            detail="Equipamento não encontrado"
        )

    db.delete(equipamento)
    db.commit()

    return {
        "message": "Equipamento deletado com sucesso!"
    }