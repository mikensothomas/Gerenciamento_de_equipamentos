from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from dependencia.depenndencia import Database
from controllers.solicitacao_emprestimo_controller import cadastrarSolicitacao
from entidades.models.solicitacao_emprestimo_model import SolicitacaoEmprestimo

solicitacao_router = APIRouter()

database = Database()

@solicitacao_router.post("/solicitar_equipamento", response_model=SolicitacaoEmprestimo)
def solicitar_equipamentos(solicitacao: SolicitacaoEmprestimo, db: Session = Depends(database.get_session)):
    try:
        return cadastrarSolicitacao(solicitacao, db)

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