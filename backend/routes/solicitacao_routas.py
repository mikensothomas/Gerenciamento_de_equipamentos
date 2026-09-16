from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from dependencia.depenndencia import Database
from controllers.solicitacao_emprestimo_controller import cadastrarSolicitacao
from entidades.models.solicitacao_emprestimo_model import SolicitacaoEmprestimo
from entidades.models.usuario_model import Usuarios
from auth.auth_login import validar_token

solicitacao_router = APIRouter()

database = Database()


@solicitacao_router.post(
    "/solicitar_equipamento",
    response_model=SolicitacaoEmprestimo
)
def solicitar_equipamentos(
    solicitacao: SolicitacaoEmprestimo,
    email_usuario: str = Depends(validar_token),
    db: Session = Depends(database.get_session)
):

    usuario = db.exec(
        select(Usuarios).where(
            Usuarios.email == email_usuario
        )
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    solicitacao.usuario_id = usuario.id_usuario

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