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
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY não configurada no .env")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user_login")


# Tokens ativos em memória
tokens_ativos: Dict[str, str] = {}


class Token(BaseModel):
    access_token: str
    token_type: str


def criar_token(
    email: str,
    expires_delta: Optional[timedelta] = None
):
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=60)
    )

    payload = {
        "sub": email,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    # Salva o token em memória
    tokens_ativos[token] = email

    return token


def validar_token(
    token: str = Depends(oauth2_scheme)
):
    try:
        if token not in tokens_ativos:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou usuário deslogado"
            )

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        return email

    except jwt.ExpiredSignatureError:
        tokens_ativos.pop(token, None)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )


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