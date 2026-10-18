from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from sqlmodel import Session
from utils.image_uploads import save_image
from auth.auth_login import admin_gestor_required
from dependencia.depenndencia import Database
from entidades.models.equipamento_model import Equipamento
from controllers.equipamento_controller import cadastrarEquipamento
from entidades.models.equipamento_model import EquipamentoResponse
from controllers.equipamento_controller import deletarEquipamento, listarEquipamento, editarEquipamento
from enums.equipamento import EquipamentoStatus

equipamento_router = APIRouter()

database = Database()

@equipamento_router.post(
    "/salvaEquipamento",
    response_model=EquipamentoResponse
)
async def cadastrar_equipamento(
    nome: str = Form(...),
    patrimonio: str = Form(...),
    marca: str = Form(...),
    modelo: str = Form(...),
    descricao: str = Form(...),
    equipamento_categoria_id: int = Form(...),
    quantidade: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_session),
    _: dict = Depends(admin_gestor_required)
):
    try:
        picture_url = await save_image(file)

        equipamento = Equipamento(
            nome=nome,
            patrimonio=patrimonio,
            marca=marca,
            modelo=modelo,
            descricao=descricao,
            equipamento_categoria_id=equipamento_categoria_id,
            quantidade=quantidade,
            picture=picture_url
        )

        return cadastrarEquipamento(
            equipamento_data=equipamento,
            db=db
        )

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
def deletarEquipamentos(id: int, db: Session = Depends(database.get_session), _: dict = Depends(admin_gestor_required)):

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


@equipamento_router.put(
    "/editarEquipamento/{id}",
    response_model=EquipamentoResponse
)
async def editar_equipamentos(
    id: int,
    nome: str = Form(...),
    patrimonio: str = Form(...),
    marca: str = Form(...),
    modelo: str = Form(...),
    descricao: str = Form(...),
    status_equipamento: EquipamentoStatus = Form(...),
    equipamento_categoria_id: int = Form(...),
    quantidade: int = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(database.get_session),
    # _: dict = Depends(admin_gestor_required)
):
    try:
        equipamento_atual = db.get(Equipamento, id)

        if not equipamento_atual:
            raise HTTPException(
                status_code=404,
                detail="Equipamento não encontrado"
            )

        picture_url = equipamento_atual.picture

        if file is not None:
            picture_url = await save_image(file)

        equipamento_data = Equipamento(
            nome=nome,
            patrimonio=patrimonio,
            marca=marca,
            modelo=modelo,
            descricao=descricao,
            status_equipamento=status_equipamento,
            equipamento_categoria_id=equipamento_categoria_id,
            quantidade=quantidade,
            picture=picture_url
        )

        return editarEquipamento(
            id=id,
            equipamentosData=equipamento_data,
            db=db
        )

    except HTTPException:
        raise

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