from fastapi import APIRouter, Depends, HTTPException, status
from controllers.categoria_equipamento_controllers import inserirCategoria
from sqlmodel import Session
from dependencia.depenndencia import database
from entidades.models.categoria_model import CategoriaEquipamento

categoriaEquipamentoRouter = APIRouter()

@categoriaEquipamentoRouter.post("/criar_categoria")
def inserir_Categoria(categoria: CategoriaEquipamento, db: Session = Depends(database.get_session)):
    try:
        inserirCategoria(categoria,db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))