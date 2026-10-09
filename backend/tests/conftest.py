import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine

from main import app
from dependencia.depenndencia import database as database_compartilhado
from routes import equipamento_routes, solicitacao_routas

load_dotenv()


@pytest.fixture
def db_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        pytest.fail("DATABASE_URL não configurada no arquivo .env")

    engine = create_engine(database_url)

    connection = engine.connect()
    transaction = connection.begin()

    try:
        yield connection
    finally:
        if transaction.is_active:
            transaction.rollback()

        connection.close()
        engine.dispose()


@pytest.fixture
def client(db_connection):
    def override_get_session():
        with Session(
            bind=db_connection,
            join_transaction_mode="create_savepoint",
        ) as session:
            yield session

    dependencias = [
        database_compartilhado.get_session,
        equipamento_routes.database.get_session,
        solicitacao_routas.database.get_session,
    ]

    for dependencia in dependencias:
        app.dependency_overrides[dependencia] = override_get_session

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        for dependencia in dependencias:
            app.dependency_overrides.pop(dependencia, None)