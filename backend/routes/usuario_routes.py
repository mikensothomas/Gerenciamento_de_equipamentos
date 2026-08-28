from fastapi import APIRouter, Depends
from controllers.usuarios_controller import inserirUsuarios
from controllers.usuario_controllers_login import loginUsuario
from sqlmodel import Session
from dependencia.depenndencia import database
from entidades.models.usuario_model import Usuarios

usaurioRoutes = APIRouter()

@usaurioRoutes.post("/user_register")
def inserir_usuarios(user: Usuarios, db: Session = Depends(database.get_session)):
    return inserirUsuarios(user,db)

@usaurioRoutes.post("/user_login")
def logar_usuarios(user: Usuarios, db: Session = Depends(database.get_session)):
    return loginUsuario(user.email, user.senha, db)