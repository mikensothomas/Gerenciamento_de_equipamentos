from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from dependencia.depenndencia import Database
from controllers.solicitacao_emprestimo_controller import cadastrarSolicitacao, deletarSolicitacao, listarSolicitacao, editarSolicitacao, aprovarSolicitacao
from entidades.models.solicitacao_emprestimo_model import SolicitacaoEmprestimo
from entidades.models.usuario_model import Usuarios
from auth.auth_login import validar_token

solicitacao_router = APIRouter()

database = Database()


@solicitacao_router.post("/solicitar_equipamento", response_model=SolicitacaoEmprestimo)
def solicitar_equipamentos(solicitacao: SolicitacaoEmprestimo, email_usuario: str = Depends(validar_token), db: Session = Depends(database.get_session)):

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

@solicitacao_router.delete("/deletar_solicitacao/{id}")
def deletarCategorias(id: int, db: Session = Depends(database.get_session)):

    try:
        deletarSolicitacao(id, db)

        return {"Deletar com sucesso"}
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@solicitacao_router.put("/editar_solicitacao/{id}")
def deletarCategorias(id: int, solicitacao: SolicitacaoEmprestimo, db: Session = Depends(database.get_session)):

    try:
        return editarSolicitacao(id, solicitacao, db)
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@solicitacao_router.get("/listar_solicitacao/{id}")
def deletarCategorias(db: Session = Depends(database.get_session)):

    try:
        return listarSolicitacao(db)
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@solicitacao_router.put("/alterar_solicitacao/{id}")
def alterarSolicitacao(id: int, solicitacao: SolicitacaoEmprestimo, email_user: str = Depends(validar_token), db: Session = Depends(database.get_session)):
    try:

        aprovador = db.exec(
            select(Usuarios).where(
                Usuarios.email == email_user
            )
        ).first()

        if not aprovador:
            raise HTTPException(
                status_code=403,
                detail="Token não fornecido"
            )

        if aprovador.perfil not in ("Administrador", "Gestor", "Tecnico"):
            raise HTTPException(
                status_code=403,
                detail="Esse usuário não pode aprovar nem reprovar solicitação"
            )
        
        return aprovarSolicitacao(id, solicitacao, aprovador, db)
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))