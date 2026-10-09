
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


def test_rota_protegida_sem_token(client):
    response = client.post("/solicitar_equipamento/1")

    assert response.status_code in (401, 403)


def test_rota_protegida_token_invalido(client):
    headers = {"Authorization": "Bearer token_invalido"}

    response = client.post(
        "/solicitar_equipamento/1",
        headers=headers
    )

    assert response.status_code in (401, 403)


def test_alterar_solicitacao_sem_token(client):
    response = client.put(
        "/alterar_solicitacao/999999",
        json={}
    )

    assert response.status_code in (401, 403, 422)


def test_alterar_solicitacao_token_invalido(client):
    headers = {"Authorization": "Bearer token_invalido"}

    response = client.put(
        "/alterar_solicitacao/999999",
        json={},
        headers=headers
    )

    assert response.status_code in (401, 403, 422)


def test_alterar_solicitacao_com_token_valido(client):
    token = obter_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put(
        "/alterar_solicitacao/999999",
        json={},
        headers=headers
    )

    assert response.status_code in (200, 400, 403, 404, 422)