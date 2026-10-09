
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


ROTAS_ESPERADAS = {
    "/criar_categoria": ["post"],
    "/listar_categoria": ["get"],
    "/editar_categoria/{id}": ["put"],
    "/deletar_categoria/{id}": ["delete"],

    "/user_register": ["post"],
    "/user_login": ["post"],
    "/logout": ["post"],
    "/editar_usuario/{id}": ["put"],
    "/deletar_usuario/{id}": ["delete"],
    "/listar_usuario": ["get"],

    "/salvaEquipamento": ["post"],
    "/deletarEquipamneto/{id}": ["delete"],
    "/listarEquipamneto": ["get"],
    "/editarEquipamneto/{id}": ["put"],

    "/solicitar_equipamento/{id}": ["post"],
    "/deletar_solicitacao/{id}": ["delete"],
    "/editar_solicitacao/{id}": ["put"],
    "/listar_solicitacao": ["get"],
    "/alterar_solicitacao/{id}": ["put"],
}


def test_documentacao_openapi():
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "paths" in response.json()


def test_todas_as_rotas_estao_registradas():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    rotas_registradas = response.json()["paths"]

    for caminho in ROTAS_ESPERADAS:
        assert caminho in rotas_registradas, (
            f"Rota não encontrada: {caminho}"
        )


def test_metodos_http_das_rotas():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    rotas_registradas = response.json()["paths"]

    for caminho, metodos in ROTAS_ESPERADAS.items():
        for metodo in metodos:
            assert metodo in rotas_registradas[caminho], (
                f"Método {metodo.upper()} não encontrado "
                f"na rota {caminho}"
            )


def test_documentacao_swagger():
    response = client.get("/docs")

    assert response.status_code == 200


def test_documentacao_redoc():
    response = client.get("/redoc")

    assert response.status_code == 200