from fastapi import APIRouter, Depends, HTTPException, status
from controllers.categoria_equipamento_controllers import inserirCategoria, listarCategoria, deletarCategoria, editarCategoria
from sqlmodel import Session
from dependencia.depenndencia import database
from entidades.models.categoria_model import CategoriaEquipamento

categoriaEquipamentoRouter = APIRouter()

@categoriaEquipamentoRouter.post("/criar_categoria")
def inserir_Categoria(categoria: CategoriaEquipamento, db: Session = Depends(database.get_session)):
    try:
        return inserirCategoria(categoria,db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@categoriaEquipamentoRouter.get("/listar_categoria")
def listarCategorias(db: Session = Depends(database.get_session)):

    try:
        return listarCategoria(db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@categoriaEquipamentoRouter.put("/editar_categoria/{id}")
def editarCategorias(id: int, categoria: CategoriaEquipamento, db: Session = Depends(database.get_session)):

    try:
        return editarCategoria(id, categoria, db)
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@categoriaEquipamentoRouter.delete("/deletar_categoria/{id}")
def deletarCategorias(id: int, db: Session = Depends(database.get_session)):

    try:
        deletarCategoria(id ,db)

        return {"Deletar com sucesso"}
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))