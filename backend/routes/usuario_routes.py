from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from controllers.usuarios_controller import inserirUsuarios, listarUsuario, editarUsuario, deletarUsuario
from controllers.usuario_controllers_login import loginUsuario
from dependencia.depenndencia import database
from entidades.models.usuario_model import Usuarios
from auth.auth_login import (Token, validar_token, logout_usuario)

usaurioRoutes = APIRouter()


@usaurioRoutes.post("/user_register")
def inserir_usuarios(user: Usuarios,db: Session = Depends(database.get_session)):

    try:
        return inserirUsuarios(user, db)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@usaurioRoutes.post("/user_login", response_model=Token)
def logar_usuarios(user: Usuarios, db: Session = Depends(database.get_session) ):
    return loginUsuario(
        user.email,
        user.senha,
        db
    )


@usaurioRoutes.get("/protegido")
def rota_protegida(usuario: str = Depends(validar_token)):
    return {
        "message": f"Bem-vindo, {usuario}!"
    }


@usaurioRoutes.post("/logout")
def logout(resultado = Depends(logout_usuario)):
    return resultado

@usaurioRoutes.put("/editar_usuario/{id}")
def editarUsuarios(id: int, usuario: Usuarios, db: Session = Depends(database.get_session)):

    try:
        return editarUsuario(id, usuario ,db)
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@usaurioRoutes.delete("/deletar_usuario/{id}")
def deletarUsuarios(id: int, db: Session = Depends(database.get_session)):

    try:
        deletarUsuario(id ,db)
        return {"Deletado com sucesso"}
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@usaurioRoutes.get("/listar_usuario")
def listarUsuarios(db: Session = Depends(database.get_session)):

    try:
        return listarUsuario(db)
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
