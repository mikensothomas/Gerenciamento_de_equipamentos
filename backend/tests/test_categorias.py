from fastapi import status


# ==========================================
# AUTENTICAÇÃO
# ==========================================

def obter_token(client, email, senha):
    response = client.post(
        "/user_login",
        json={
            "email": email,
            "senha": senha
        }
    )

    assert response.status_code == status.HTTP_200_OK, (
        f"Falha no login: {response.text}"
    )

    dados = response.json()

    assert "access_token" in dados, (
        f"Token não encontrado na resposta: {dados}"
    )

    return dados["access_token"]


def obter_headers(client):
    email = "mikensonthomas0@gmail.com"
    senha = "111111"

    token = obter_token(client, email, senha)

    return {
        "Authorization": f"Bearer {token}"
    }


# ==========================================
# CRIAR CATEGORIA
# ==========================================

def test_criar_categoria(client):
    headers = obter_headers(client)

    categoria = {
        "categoria_name": "Categoria Teste"
    }

    response = client.post(
        "/criar_categoria",
        json=categoria,
        headers=headers
    )

    assert response.status_code in (200, 201), response.text
    assert response.json()["categoria_name"] == "Categoria Teste"


# ==========================================
# LISTAR CATEGORIAS
# ==========================================

def test_listar_categorias(client):
    headers = obter_headers(client)

    response = client.get(
        "/listar_categoria",
        headers=headers
    )

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)


# ==========================================
# EDITAR CATEGORIA
# ==========================================

def test_editar_categoria(client):
    headers = obter_headers(client)

    criacao = client.post(
        "/criar_categoria",
        json={"categoria_name": "Categoria Antiga"},
        headers=headers
    )

    assert criacao.status_code in (200, 201), criacao.text

    dados = criacao.json()
    categoria_id = dados["categoria_id"]

    assert categoria_id is not None, (
        f"ID não encontrado na resposta: {dados}"
    )

    response = client.put(
        f"/editar_categoria/{categoria_id}",
        json={"categoria_name": "Categoria Atualizada"},
        headers=headers
    )

    assert response.status_code == status.HTTP_200_OK, response.text

    # Verifica a alteração, caso a rota retorne a categoria atualizada.
    if response.status_code == status.HTTP_200_OK:
        if isinstance(response.json(), dict) and "categoria_name" in response.json():
            assert response.json()["categoria_name"] == "Categoria Atualizada"


# ==========================================
# DELETAR CATEGORIA
# ==========================================

def test_deletar_categoria(client):
    headers = obter_headers(client)

    criacao = client.post(
        "/criar_categoria",
        json={"categoria_name": "Categoria Para Excluir"},
        headers=headers
    )

    assert criacao.status_code in (200, 201), criacao.text

    dados = criacao.json()
    categoria_id = dados["categoria_id"]

    assert categoria_id is not None, (
        f"ID não encontrado na resposta: {dados}"
    )

    response = client.delete(
        f"/deletar_categoria/{categoria_id}",
        headers=headers
    )

    assert response.status_code in (200, 204), response.text