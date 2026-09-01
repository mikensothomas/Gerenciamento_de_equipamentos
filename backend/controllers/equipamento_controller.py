from sqlmodel import Session
from sqlalchemy.exc import OperationalError, IntegrityError
from entidades.models.equipamento_model import Equipamento
from entidades.models.categoria_model import CategoriaEquipamento


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