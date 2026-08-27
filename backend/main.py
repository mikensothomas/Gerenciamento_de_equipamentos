from fastapi import FastAPI
from DB.db import Database
from routes import categoria_routes, usuario_routes

app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application with a custom title and description.",
    version="1.0.0",
)

db = Database()

@app.on_event("startup")
def startup_event():
    db.connect()

@app.get("/check-db")
def check_db():
    try:
        with db.get_session() as session:
            return {"status": "✅ Conexão feita com sucesso!"}
    except Exception as e:
        return {"status": "❌ Falha na conexão", "error": str(e)}

app.include_router(categoria_routes.categoriaEquipamentoRouter)
app.include_router(usuario_routes.usaurioRoutes)