
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_api_inicia():
    assert app is not None


def test_documentacao_swagger():
    response = client.get("/docs")
    assert response.status_code == 200


def test_documentacao_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200