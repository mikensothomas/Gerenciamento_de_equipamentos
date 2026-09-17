from sqlmodel import Session
from sqlalchemy.exc import OperationalError, IntegrityError
from entidades.models.equipamento_model import Equipamento
from entidades.models.categoria_model import CategoriaEquipamento
from entidades.models.equipamento_model import Equipamento
from sqlmodel import Session, select
from fastapi import HTTPException


def cadastrarEquipamento(equipamento_data: Equipamento, db: Session):
    try:
        categoria = db.get(CategoriaEquipamento, equipamento_data.equipamento_categoria_id)
        
        if not categoria:
            raise ValueError("Categoria informada não existe")
        
        equipamento = Equipamento(**equipamento_data.model_dump(exclude={"equipamento_id", "equipamento_categoria"}))
        db.add(equipamento)
        db.commit()
        db.refresh(equipamento)
        return equipamento
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError as e:
        raise ValueError("Verifique os dados") from e
    

def deletarEquipamento(id: int, db: Session):

    try: 
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
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e


def listarEquipamento(db: Session):

    try: 
        equipamentos = db.exec(select(Equipamento)).all()

        return equipamentos
    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    

def editarEquipamento(id: int, equipamentosData: Equipamento, db: Session):
    try:
        equipamento = db.get(Equipamento, id)

        if not equipamento:
            raise ValueError("Equipamento informada não existe")

        equipamento.nome = equipamentosData.nome
        equipamento.patrimonio = equipamentosData.patrimonio
        equipamento.marca = equipamentosData.marca
        equipamento.modelo = equipamentosData.modelo
        equipamento.descricao = equipamentosData.descricao
        equipamento.status_equipamento = equipamentosData.status_equipamento
        equipamento.equipamento_categoria_id = equipamentosData.equipamento_categoria_id

        db.add(equipamento)
        db.commit()
        db.refresh(equipamento)

        return equipamento
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError as e:
        raise ValueError("Erro de integridade nos dados informados") from e

    
