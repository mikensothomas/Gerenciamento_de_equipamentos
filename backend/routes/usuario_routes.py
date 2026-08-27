from fastapi import APIRouter, Depends
from controllers.usuarios_controller import inserirUsuarios
from sqlmodel import Session
from dependencia.depenndencia import database
from entidades.models.usuario_model import Usuarios

usaurioRoutes = APIRouter()

@usaurioRoutes.post("/user_register")
def inserir_usuarios(user: Usuarios, db: Session = Depends(database.get_session)):
    inserirUsuarios(user,db)