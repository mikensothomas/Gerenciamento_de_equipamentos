from contextlib import asynccontextmanager
from fastapi import FastAPI
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi.staticfiles import StaticFiles

from DB.db import Database

from routes import (
    categoria_routes,
    usuario_routes,
    equipamento_routes,
    solicitacao_routas,
)

db = Database()

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    yield


app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application with a custom title and description.",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads"
)


@app.get("/check-db")
def check_db():
    try:
        with db.get_session() as session:
            return {"status": "Conexão feita com sucesso!"}
    except Exception as e:
        return {
            "status": " ❌ Falha na conexão",
            "error": str(e),
        }


app.include_router(categoria_routes.categoriaEquipamentoRouter)
app.include_router(usuario_routes.usaurioRoutes)
app.include_router(equipamento_routes.equipamento_router)
app.include_router(solicitacao_routas.solicitacao_router)