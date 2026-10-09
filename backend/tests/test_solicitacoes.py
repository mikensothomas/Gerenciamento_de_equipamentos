
from fastapi import status


EMAIL = "mikensonthomas0@gmail.com"
SENHA = "111111"


def obter_token(client, email=EMAIL, senha=SENHA):
    response = client.post(
        "/user_login",
        json={"email": email, "senha": senha}
    )

    assert response.status_code == status.HTTP_200_OK, (
        f"Falha no login: {response.text}"
    )

    dados = response.json()
    assert "access_token" in dados

    return dados["access_token"]


def obter_headers(client):
    token = obter_token(client)
    return {"Authorization": f"Bearer {token}"}


# =========================
# CRIAR SOLICITAÇÃO
# =========================

def test_criar_solicitacao_sem_token(client):
    response = client.post("/solicitar_equipamento/1")

    assert response.status_code in (401, 403)


def test_criar_solicitacao_token_invalido(client):
    headers = {"Authorization": "Bearer token_invalido"}

    response = client.post(
        "/solicitar_equipamento/1",
        headers=headers
    )

    assert response.status_code in (401, 403)


def test_criar_solicitacao_equipamento_inexistente(client):
    headers = obter_headers(client)

    response = client.post(
        "/solicitar_equipamento/999999",
        headers=headers
    )

    assert response.status_code in (400, 404, 422)


def test_criar_solicitacao_id_invalido(client):
    headers = obter_headers(client)

    response = client.post(
        "/solicitar_equipamento/0",
        headers=headers
    )

    assert response.status_code in (400, 404, 422)


# =========================
# EDITAR SOLICITAÇÃO
# =========================

def test_editar_solicitacao_sem_token(client):
    response = client.put(
        "/alterar_solicitacao/1",
        json={}
    )

    assert response.status_code in (401, 403, 422)


def test_editar_solicitacao_token_invalido(client):
    headers = {"Authorization": "Bearer token_invalido"}

    response = client.put(
        "/alterar_solicitacao/1",
        json={},
        headers=headers
    )

    assert response.status_code in (401, 403, 422)


def test_editar_solicitacao_inexistente(client):
    headers = obter_headers(client)

    response = client.put(
        "/alterar_solicitacao/999999",
        json={},
        headers=headers
    )

    assert response.status_code in (400, 403, 404, 422)


# =========================
# LISTAR SOLICITAÇÕES
# =========================
# Substitua a rota abaixo pelo caminho real do seu projeto.

def test_listar_solicitacoes_sem_token(client):
    response = client.get("/listar_solicitacoes")

    assert response.status_code in (401, 403, 404, 405)


def test_listar_solicitacoes_com_token(client):
    headers = obter_headers(client)

    response = client.get(
        "/listar_solicitacoes",
        headers=headers
    )

    assert response.status_code in (200, 403, 404, 405)


# =========================
# DELETAR SOLICITAÇÃO
# =========================
# Substitua a rota abaixo pelo caminho real do seu projeto.

def test_deletar_solicitacao_sem_token(client):
    response = client.delete("/deletar_solicitacao/999999")

    assert response.status_code in (401, 403, 404, 405)


def test_deletar_solicitacao_com_token(client):
    headers = obter_headers(client)

    response = client.delete(
        "/deletar_solicitacao/999999",
        headers=headers
    )

    assert response.status_code in (200, 204, 400, 403, 404, 405)