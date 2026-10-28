from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPAuthorizationCredentials
import jwt

from sqlmodel import Session, select

from controllers.usuarios_controller import (
    inserirUsuarios,
    listarUsuario,
    editarUsuario,
    deletarUsuario,
    updatPicture,
    removePicture,
    loginUsuario
)

from dependencia.depenndencia import database

from entidades.models.usuario_model import Usuarios, UsuarioCadastro
from entidades.models.token_model import RevokedToken

from auth.auth_login import (
    ALGORITHM,
    SECRET_KEY,
    LogoutRequest,
    RefreshTokenRequest,
    Token,
    admin_required,
    criar_token,
    logout_usuario,
    revogar_token,
    validar_token,
    bearer_scheme
)

from datetime import datetime, timezone

usaurioRoutes = APIRouter()


@usaurioRoutes.post("/user_register")
def inserir_usuarios(user: UsuarioCadastro, db: Session = Depends(database.get_session)):

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


@usaurioRoutes.post("/refresh", response_model=Token)
def renovar_token(
    dados: RefreshTokenRequest,
    db: Session = Depends(database.get_session)
):
    try:
        payload = jwt.decode(
            dados.refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("tipo") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="O token informado não é um refresh token."
            )

        email = payload.get("sub")
        perfil = payload.get("perfil")

        if not email or not perfil or not payload.get("jti"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Dados do token inválidos."
            )

        revogar_token(payload, db)

        novo_access_token = criar_token(
            email=email,
            perfil=perfil,
            tipo="access"
        )

        novo_refresh_token = criar_token(
            email=email,
            perfil=perfil,
            tipo="refresh"
        )

        db.commit()

        return Token(
            access_token=novo_access_token,
            refresh_token=novo_refresh_token
        )

    except jwt.ExpiredSignatureError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expirado. Faça login novamente."
        )

    except jwt.PyJWTError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido."
        )

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível renovar a sessão."
        )

@usaurioRoutes.post("/logout")
def logout(
    dados: LogoutRequest,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(database.get_session)
):
    return logout_usuario(
        credentials=credentials,
        dados=dados,
        session=db
    )

@usaurioRoutes.put("/editar_usuario/{id}")
def editarUsuarios(id: int, usuario: Usuarios, db: Session = Depends(database.get_session), _: dict = Depends(admin_required)):

    try:
        return editarUsuario(id, usuario ,db)
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@usaurioRoutes.delete("/deletar_usuario/{id}")
def deletarUsuarios(id: int, db: Session = Depends(database.get_session), _: dict = Depends(admin_required)):

    try:
        deletarUsuario(id ,db)
        return {"Deletado com sucesso"}
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@usaurioRoutes.get("/listar_usuario")
def listarUsuarios(db: Session = Depends(database.get_session), _: dict = Depends(admin_required)):

    try:
        return listarUsuario(db)
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@usaurioRoutes.patch("/update_picture")
async def update_pictures(
    picture: UploadFile = File(...),
    db: Session = Depends(database.get_session),
    current_user: dict = Depends(validar_token)
):
    try:
        return updatPicture(
            picture=picture,
            db=db,
            current_user=current_user
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@usaurioRoutes.delete("/remove_pictures")
def remove_pictures(
    db: Session = Depends(database.get_session),
    current_user: dict = Depends(validar_token)
):
    try:
        return removePicture(
            db=db,
            current_user=current_user
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )