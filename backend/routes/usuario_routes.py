from fastapi import APIRouter, Depends
from sqlmodel import Session

from controllers.usuarios_controller import inserirUsuarios
from controllers.usuario_controllers_login import loginUsuario

from dependencia.depenndencia import database
from entidades.models.usuario_model import Usuarios

from auth.auth_login import (
    Token,
    validar_token,
    logout_usuario
)


usaurioRoutes = APIRouter()


@usaurioRoutes.post("/user_register")
def inserir_usuarios(
    user: Usuarios,
    db: Session = Depends(database.get_session)
):
    return inserirUsuarios(user, db)


@usaurioRoutes.post(
    "/user_login",
    response_model=Token
)
def logar_usuarios(
    user: Usuarios,
    db: Session = Depends(database.get_session)
):
    return loginUsuario(
        user.email,
        user.senha,
        db
    )


@usaurioRoutes.get("/protegido")
def rota_protegida(
    usuario: str = Depends(validar_token)
):
    return {
        "message": f"Bem-vindo, {usuario}!"
    }


@usaurioRoutes.post("/logout")
def logout(
    resultado = Depends(logout_usuario)
):
    return resultado