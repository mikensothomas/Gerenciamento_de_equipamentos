from fastapi import status


# ==================================================
# FUNÇÃO AUXILIAR: FAZER LOGIN E OBTER TOKEN
# ==================================================

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


# ==================================================
# TESTE 1: LISTAR EQUIPAMENTOS
# ==================================================

def test_listar_equipamentos(client):
    email = "mikensonthomas0@gmail.com"
    senha = "111111"

    token = obter_token(client, email, senha)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get(
        "/listarEquipamneto",
        headers=headers
    )

    assert response.status_code == status.HTTP_200_OK, (
        response.text
    )


# ==================================================
# TESTE 2: CADASTRAR EQUIPAMENTO
# ==================================================

def test_cadastrar_equipamento(client):
    email = "mikensonthomas0@gmail.com"
    senha = "111111"

    token = obter_token(client, email, senha)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    equipamento = {
        "patrimonio": "PAT",
        "marca": "Dell",
        "descricao": "Equipamento para teste",
        "equipamento_categoria_id": 2,
        "quantidade": 1,
        "nome": "Notebook de teste",
        "modelo": "Latitude 5420",
        "status_equipamento": "Disponivel"
    }

    response = client.post(
        "/salvaEquipamento",
        json=equipamento,
        headers=headers
    )

    assert response.status_code in (
        status.HTTP_200_OK,
        status.HTTP_201_CREATED
    ), response.text


# ==================================================
# TESTE 3: EDITAR EQUIPAMENTO
# ==================================================

def test_editar_equipamento(client):
    email = "mikensonthomas0@gmail.com"
    senha = "111111"

    token = obter_token(client, email, senha)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    equipamento = {
        "patrimonio": "PAT",
        "marca": "Dell",
        "descricao": "Equipamento atualizado para teste",
        "equipamento_categoria_id": 2,
        "quantidade": 1,
        "nome": "Notebook atualizado",
        "modelo": "Latitude 5420",
        "status_equipamento": "Disponivel"
    }

    response = client.put(
        "/editarEquipamneto/2",
        json=equipamento,
        headers=headers
    )

    assert response.status_code in (
        status.HTTP_200_OK,
        status.HTTP_204_NO_CONTENT
    ), response.text


# ==================================================
# TESTE 4: EXCLUIR EQUIPAMENTO
# ==================================================

def test_deletar_equipamento(client):
    email = "mikensonthomas0@gmail.com"
    senha = "111111"

    token = obter_token(client, email, senha)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.delete(
        "/deletarEquipamneto/2",
        headers=headers
    )

    assert response.status_code in (
        status.HTTP_200_OK,
        status.HTTP_204_NO_CONTENT
    ), response.text
