from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
import os
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY não configurada no .env")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


tokens_ativos: Dict[str, str] = {}


class Token(BaseModel):
    access_token: str
    token_type: str

def criar_token(
    email: str,
    perfil: str,
    expires_delta: Optional[timedelta] = None
):
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=60)
    )

    payload = {
        "sub": email,
        "perfil": perfil,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def validar_token(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")
        perfil = payload.get("perfil")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        return {"email": email, "perfil": perfil}

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

def admin_gestor_required(
    usuario: dict = Depends(validar_token)
):
    if usuario["perfil"] not in ["Administrador", "Gestor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado, essa rota é restrita a administradores e gestores"
        )

    return usuario


def logout_usuario(
    token: str = Depends(oauth2_scheme)
):
    if token not in tokens_ativos:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    del tokens_ativos[token]

    return {
        "message": "Logout realizado com sucesso"
    }