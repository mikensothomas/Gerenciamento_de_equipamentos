from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from dependencia.depenndencia import Database
from entidades.models.equipamento_model import Equipamento
from controllers.equipamento_controller import cadastrarEquipamento
from entidades.models.equipamento_model import EquipamentoResponse
from controllers.equipamento_controller import deletarEquipamento, listarEquipamento, editarEquipamento

equipamento_router = APIRouter()

database = Database()

@equipamento_router.post("/salvaEquipamento",response_model=EquipamentoResponse)
def cadastrar_equipamento(equipamento: Equipamento, db: Session = Depends(database.get_session)):
    try:
        return cadastrarEquipamento(equipamento, db)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@equipamento_router.delete("/deletarEquipamneto/{id}")
def deletarEquipamentos(id: int, db: Session = Depends(database.get_session)):

    try:
        return deletarEquipamento(id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@equipamento_router.get("/listarEquipamneto")
def listarEquipamentos(db: Session = Depends(database.get_session)):

    try:
        return listarEquipamento(db)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@equipamento_router.put("/editarEquipamneto/{id}")
def listarEquipamentos(id: int, equipamamento: Equipamento, db: Session = Depends(database.get_session)):

    try:
        return editarEquipamento(id, equipamamento, db)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )