from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from dependencia.depenndencia import Database
from entidades.models.equipqmento_model import Equipamento
from controllers.equipamento_controller import cadastrarEquipamento

equipamento_router = APIRouter()

database = Database

equipamento_router.post("/salvaEquipamento")
def cadastrarEquipamento(equipamento: Equipamento, db: Session = Depends(database.get_session)):
    try:
        cadastrarEquipamento(equipamento, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))