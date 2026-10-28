import os
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlmodel import Session, select

from dependencia.depenndencia import database
from entidades.models.token_model import RevokedToken

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")
)

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY não configurada no .env")

bearer_scheme = HTTPBearer()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


def criar_token(
    email: str,
    perfil: str,
    tipo: str = "access"
) -> str:

    agora = datetime.now(timezone.utc)

    if tipo == "access":
        expiracao = agora + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    elif tipo == "refresh":
        expiracao = agora + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
    else:
        raise ValueError("Tipo de token inválido")

    payload = {
        "sub": email,
        "perfil": perfil,
        "tipo": tipo,
        "jti": str(uuid4()),
        "iat": agora,
        "exp": expiracao
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def validar_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: Session = Depends(database.get_session)
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")
        perfil = payload.get("perfil")
        jti = payload.get("jti")

        if (
            not email
            or not perfil
            or not jti
            or payload.get("tipo") != "access"
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token inválido"
            )

        revogado = session.exec(
            select(RevokedToken).where(
                RevokedToken.jti == jti
            )
        ).first()

        if revogado:
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
            detail="Acesso restrito a administradores"
        )

    return usuario


def gestor_required(
    usuario: dict = Depends(validar_token)
):
    if usuario["perfil"] != "Gestor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a gestores"
        )

    return usuario


def revogar_token(payload: dict, session: Session):
    jti = payload.get("jti")
    exp = payload.get("exp")

    if not jti or not exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    existente = session.exec(
        select(RevokedToken).where(
            RevokedToken.jti == jti
        )
    ).first()

    if existente:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token já revogado"
        )

    session.add(
        RevokedToken(
            jti=jti,
            expire_at=datetime.fromtimestamp(
                exp,
                tz=timezone.utc
            ).replace(tzinfo=None),
            revoked_at=datetime.now(
                timezone.utc
            ).replace(tzinfo=None)
        )
    )


def logout_usuario(
    credentials: HTTPAuthorizationCredentials,
    dados: LogoutRequest,
    session: Session
):
    try:
        access_payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        refresh_payload = jwt.decode(
            dados.refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if access_payload.get("tipo") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token inválido"
            )

        if refresh_payload.get("tipo") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido"
            )

        if access_payload.get("sub") != refresh_payload.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Os tokens não pertencem à mesma sessão de usuário"
            )

        revogar_token(access_payload, session)
        revogar_token(refresh_payload, session)

        session.commit()

        return {
            "message": "Logout realizado com sucesso"
        }

    except jwt.ExpiredSignatureError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Um dos tokens expirou. Faça login novamente."
        )

    except jwt.PyJWTError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    except Exception:
        session.rollback()
        raise