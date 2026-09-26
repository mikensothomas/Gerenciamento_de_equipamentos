from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError, IntegrityError
from entidades.models.solicitacao_emprestimo_model import SolicitacaoEmprestimo
from entidades.models.equipamento_model import Equipamento
from entidades.models.usuario_model import Usuarios
from fastapi import HTTPException

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

    except Exception as e:
        db.rollback()
        print("ERRO REAL:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    except IntegrityError as e:
        raise ValueError("Erro de integridade nos dados informados") from e


def deletarSolicitacao(id: int, solicitacoes: SolicitacaoEmprestimo, db: Session):

    try:
        solicitacao = db.exec(select(SolicitacaoEmprestimo).where(solicitacoes.equipamento_id == id)).first()

        if not solicitacao:
            raise HTTPException(
                status_code=404,
                detail="Solicitação não encontrada"
            )

        db.delete(solicitacao)
        db.commit()
        return {
            "Solicitação deletada com sucesso"
        }

    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e


def listarSolicitacao(db: Session):

    try:
        solicitacao = db.exec(select(SolicitacaoEmprestimo)).all()

        if not solicitacao:
            raise HTTPException("Nenhuma solicitação encontarda")

        return solicitacao
    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e

    
def editarSolicitacao(id: int, solicitacoes: SolicitacaoEmprestimo, db: Session):

    try:
        solicitacao = db.get(SolicitacaoEmprestimo, id)

        if not solicitacao:
            raise HTTPException("Soliciação informada não existe")

        solicitacao.status_solicitacao = solicitacoes.status_solicitacao
        solicitacao.data_aprovacao = solicitacoes.data_aprovacao
        solicitacao.equipamento_id = solicitacoes.equipamento_id
        solicitacao.id_aprovador = solicitacoes.id_aprovador

        db.add(solicitacao)
        db.commit()
        db.refresh(solicitacao)

        return solicitacao
        
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError as e:
        raise ValueError("Erro de integridade nos dados informados") from e

def aprovarSolicitacao(id: int, solicitacoes: SolicitacaoEmprestimo, aprovador_solicitacao: Usuarios, db: Session):

    try:
        solicitacao = db.get(SolicitacaoEmprestimo, id)
        
        if not solicitacao:
            raise HTTPException("Solicitação não encontrado")
        
        solicitacao.status_solicitacao = solicitacoes.status_solicitacao
        solicitacao.id_aprovador = aprovador_solicitacao.id_usuario
    
        db.add(solicitacao)
        db.commit()
        db.refresh(solicitacao)
    
        return {
            f"Solicitação ID {solicitacao.id_solicitacao_emprestimo} alterada com sucesso"
        }
    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError as e:
        raise ValueError("Erro de integridade nos dados informados") from e
    