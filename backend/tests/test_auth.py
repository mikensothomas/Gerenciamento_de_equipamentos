import pytest
import jwt

from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

from auth.auth_login import (
    SECRET_KEY,
    ALGORITHM,
    criar_token,
    validar_token,
    admin_gestor_required,
    logout_usuario,
    tokens_ativos,
)


def test_criar_token_com_dados_validos():
    token = criar_token(
        email="aluno@teste.com",
        perfil="Aluno"
    )

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    assert payload["sub"] == "aluno@teste.com"
    assert payload["perfil"] == "Aluno"
    assert "exp" in payload


def test_validar_token_valido():
    token = criar_token(
        email="aluno@teste.com",
        perfil="Aluno"
    )

    usuario = validar_token(token)

    assert usuario["email"] == "aluno@teste.com"
    assert usuario["perfil"] == "Aluno"


def test_validar_token_invalido():
    with pytest.raises(HTTPException) as erro:
        validar_token("token_invalido")

    assert erro.value.status_code == 401
    assert erro.value.detail == "Token inválido"


def test_validar_token_expirado():
    payload = {
        "sub": "aluno@teste.com",
        "perfil": "Aluno",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    with pytest.raises(HTTPException) as erro:
        validar_token(token)

    assert erro.value.status_code == 401
    assert erro.value.detail == "Token expirado"


def test_validar_token_sem_email():
    token = jwt.encode(
        {
            "perfil": "Aluno",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=10)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    with pytest.raises(HTTPException) as erro:
        validar_token(token)

    assert erro.value.status_code == 401


@pytest.mark.parametrize(
    "perfil",
    ["Administrador", "Gestor"]
)
def test_admin_gestor_permitido(perfil):
    usuario = {
        "email": "gestor@teste.com",
        "perfil": perfil
    }

    resultado = admin_gestor_required(usuario)

    assert resultado == usuario


def test_aluno_nao_pode_acessar_rota_restrita():
    usuario = {
        "email": "aluno@teste.com",
        "perfil": "Aluno"
    }

    with pytest.raises(HTTPException) as erro:
        admin_gestor_required(usuario)

    assert erro.value.status_code == 403


def test_logout_token_inexistente():
    with pytest.raises(HTTPException) as erro:
        logout_usuario("token_que_nao_existe")

    assert erro.value.status_code == 401


def test_logout_token_ativo():
    token = "token_teste_ativo"
    tokens_ativos[token] = "aluno@teste.com"

    resultado = logout_usuario(token)

    assert resultado["message"] == "Logout realizado com sucesso"
    assert token not in tokens_ativos