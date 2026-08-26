from fastapi import APIRouter, Depends
from controllers.categoria_equipamento_controllers import inserirCategoria
from sqlmodel import Session
from dependencia.depenndencia import database
from entidades.models.categoria_model import CategoriaEquipamento

categoriaEquipamentoRouter = APIRouter()

@categoriaEquipamentoRouter.post("/criar_categoria")
def inserir_Categoria(categoria: CategoriaEquipamento, db: Session = Depends(database.get_session)):
    inserirCategoria(categoria,db)