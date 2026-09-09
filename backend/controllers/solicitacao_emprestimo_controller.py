from sqlmodel import Session
from sqlalchemy.exc import OperationalError, IntegrityError
from entidades.models.solicitacao_emprestimo_model import SolicitacaoEmprestimo
from entidades.models.equipamento_model import Equipamento
from entidades.models.usuario_model import Usuarios

def cadastrarSolicitacao(solicitacao_data: SolicitacaoEmprestimo, db: Session):
    try:
        usuario = db.get(Usuarios, solicitacao_data.usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        equipamento = db.get(Equipamento, solicitacao_data.equipamento_id)
        if not equipamento:
            raise ValueError("Equipamento não encontrado")

        db.add(solicitacao_data)
        db.commit()
        db.refresh(solicitacao_data)
        return solicitacao_data

    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Erro de integridade nos dados informados") from e