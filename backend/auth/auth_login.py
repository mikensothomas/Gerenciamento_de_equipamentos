
from datetime import datetime, timedelta, timezone
from typing import Optional
import os
from uuid import uuid4
from zoneinfo import ZoneInfo
import jwt
from sqlmodel import Session, select
from dependencia.depenndencia import database
from entidades.models.token_model import RevokedToken

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY não configurada no .env")

if not ALGORITHM:
    raise RuntimeError("ALGORITHM não configurado no .env")


bearer_scheme = HTTPBearer()

class Token(BaseModel):
    access_token: str
    token_type: str


def criar_token(
    email: str,
    perfil: str,
    expires_delta: Optional[timedelta] = None
):
    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {
        "sub": email,
        "perfil": perfil,
        "jti": str(uuid4()),
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def validar_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: Session = Depends(database.get_session)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")
        perfil = payload.get("perfil")
        jti = payload.get("jti")

        if not email or not perfil:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        token_revogado = session.exec(
            select(RevokedToken).where(
                RevokedToken.jti == jti
            )
        ).first()

        if token_revogado:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token revogado. Faça login novamente."
            )

        return {
            "email": email,
            "perfil": perfil
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )


def admin_required(
    usuario: dict = Depends(validar_token)
):
    if usuario["perfil"] != "Administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado, essa rota é restrita a administradores"
        )

    return usuario

def gestor_required(
    usuario: dict = Depends(validar_token)
):
    if usuario["perfil"] != "Gestor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado, essa rota é restrita a gestores"
        )

    return usuario


def logout_usuario(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: Session = Depends(database.get_session)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        jti = payload.get("jti")
        exp = payload.get("exp")

        if not jti or not exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        toke_revogado = session.exec(select(RevokedToken).where(RevokedToken.jti == jti)).first()

        if toke_revogado:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token já revogado"
            )

        registro = RevokedToken(
            jti=jti,
            expires_at=datetime.fromtimestamp(
                exp,
                tz=ZoneInfo("America/Sao_Paulo")
            ).replace(tzinfo=None),
            revoked_at=datetime.now(
                ZoneInfo("America/Sao_Paulo")
            ).replace(tzinfo=None)
        )

        session.add(registro)
        session.commit()
        
        return {
            "message": "Logout realizado com sucesso"
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )