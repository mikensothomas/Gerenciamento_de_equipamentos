from entidades.models.usuario_model import Usuarios
from sqlmodel import Session, select
from fastapi import HTTPException
from services.password import verificar_password


def loginUsuario(email: str, senha: str, db: Session):

    usuario = db.exec(
        select(Usuarios).where(
            Usuarios.email == email
        )
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos"
        )

    senha_valida = verificar_password(
        senha,
        usuario.senha
    )

    if not senha_valida:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos"
        )

    return {
        "message": "Login feito com sucesso!",
    }