
from uuid import uuid4
from random import randrange

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


def criar_usuario(email=None, cpf=None, perfil="Aluno"):
    return {
        "cpf": cpf or str(randrange(10_000_000_000, 99_999_999_999)),
        "nome": "Usuario Teste API",
        "email": email or f"usuario_{uuid4().hex[:12]}@example.com",
        "senha": "SenhaTeste123!",
        "perfil": perfil,
        "status_usuario": "Ativo",
    }


def test_cadastrar_usuario(client):
    usuario = criar_usuario()

    response = client.post("/user_register", json=usuario)

    assert response.status_code == 200, response.text
    assert response.json()["message"] == "Cadastro feito com sucesso!"


def test_cadastrar_usuario_email_duplicado(client):
    email = f"duplicado_{uuid4().hex[:12]}@example.com"

    usuario1 = criar_usuario(email=email)
    usuario2 = criar_usuario(email=email)

    primeira_resposta = client.post("/user_register", json=usuario1)

    assert primeira_resposta.status_code == 200, primeira_resposta.text

    segunda_resposta = client.post("/user_register", json=usuario2)

    assert segunda_resposta.status_code == status.HTTP_400_BAD_REQUEST, (
        segunda_resposta.text
    )


def test_login_usuario_senha_incorreta(client):
    usuario = criar_usuario()
    cadastro = client.post("/user_register", json=usuario)

    assert cadastro.status_code == 200, cadastro.text

    response = client.post(
        "/user_login",
        json={
            "email": usuario["email"],
            "senha": "SenhaErrada123!",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text


def test_login_usuario_email_inexistente(client):
    response = client.post(
        "/user_login",
        json={
            "email": f"inexistente_{uuid4().hex[:12]}@example.com",
            "senha": "SenhaTeste123!",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text


def test_cadastrar_usuario_perfil_invalido(client):
    usuario = {
        "cpf": "12345678901",
        "nome": "Usuario Teste",
        "email": f"invalido_{uuid4().hex[:12]}@example.com",
        "senha": "SenhaTeste123!",
        "perfil": "PerfilInexistente",
        "status_usuario": "Ativo",
    }

    response = client.post("/user_register", json=usuario)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, (
        response.text
    )

def test_listar_usuarios(client):

    headers = obter_headers(client)

    response = client.get("/listar_usuario", headers=headers)

    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)


def test_listar_usuarios_rota_existe(client):
    response = client.get("/listar_usuario")

    assert response.status_code != 404, (
        "A rota /listar_usuario não foi encontrada."
    )

def test_editar_usuario_sem_autenticacao(client):
    response = client.put(
        "/editar_usuario/1",
        json={
            "cpf": "12345678901",
            "nome": "Usuario Editado",
            "email": "editado@example.com",
            "senha": "SenhaTeste123!",
            "perfil": "Aluno",
            "status_usuario": "Ativo"
        }
    )

    assert response.status_code == 401, response.text

def test_deletar_usuario_sem_autenticacao(client):
    response = client.delete("/deletar_usuario/1")

    assert response.status_code == 401, response.text

def test_logout_sem_autenticacao(client):
    response = client.post("/logout")

    assert response.status_code == 401, response.text

def test_cadastrar_usuario_sem_campos_obrigatorios(client):
    response = client.post(
        "/user_register",
        json={}
    )

    assert response.status_code == 422, response.text
