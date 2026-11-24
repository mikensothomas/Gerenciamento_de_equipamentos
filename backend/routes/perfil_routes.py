from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from entidades.models.perfil import Perfil
from dependencia.depenndencia import Database
from controllers.perfil_controller import cadastrarPerfil
database = Database()

router = APIRouter()


@router.post("/profile_register")
def registrar_perfil(
    perfil: Perfil,
    db: Session = Depends(database.get_session)
):
    try:
        resultado = cadastrarPerfil(perfil, db)

        return {
            "mensagem": "Perfil cadastrado com sucesso!",
            "perfil": resultado
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=409,
            detail=str(erro)
        )

    except RuntimeError as erro:
        raise HTTPException(
            status_code=500,
            detail=str(erro)
        )

    except Exception as erro:
        print("Erro na rota:", repr(erro))

        raise HTTPException(
            status_code=500,
            detail="Não foi possível cadastrar o perfil."
        )