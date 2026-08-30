from entidades.models.usuario_model import Usuarios
from sqlmodel import Session, select
from fastapi import HTTPException
from services.password_hash import verificar_password
from datetime import timedelta
from auth.auth_login import ( criar_token, ACCESS_TOKEN_EXPIRE_MINUTES )


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

    token = criar_token(
        email=usuario.email,
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }