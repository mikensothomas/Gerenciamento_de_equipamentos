from entidades.models.usuario_model import Usuarios
from sqlmodel import Session, select
from fastapi import HTTPException
from services.password_hash import hash_password
from sqlalchemy.exc import OperationalError, IntegrityError
from services.password_hash import verificar_password
from datetime import timedelta
from auth.auth_login import ( criar_token, ACCESS_TOKEN_EXPIRE_MINUTES )

def inserirUsuarios(usuario: Usuarios, db = Session):

    try:
        user_existente_por_cpf = db.exec(
            select(Usuarios).where(
                Usuarios.cpf == usuario.cpf
            )
        ).first()

        user_existente_por_email = db.exec(
            select(Usuarios).where(
                Usuarios.email == usuario.email
            )
        ).first()

        if user_existente_por_cpf:
            raise HTTPException(
                status_code=400,
                detail="CPF duplicado"
            )

        if user_existente_por_email:
            raise HTTPException(
                status_code=400,
                detail="Email duplicado"
            )

        usuario.senha = hash_password(usuario.senha)
        
        inserir_usuarios = Usuarios.model_validate(usuario)
        db.add(inserir_usuarios)
        db.commit()
        db.refresh(inserir_usuarios)
        return {
            "message": "Cadastro feito com sucesso!",
        }
    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError as e:
        raise ValueError("Verifique os dados") from e

def listarUsuario(db: Session):

    try:
        usuarios = db.exec(select(Usuarios)).all()

        if not usuarios:
            raise HTTPException("Nenhum usuário encontrado")

        return usuarios
    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    
def deletarUsuario(id: int, db: Session):
    try:
        usuario = db.exec(select(Usuarios).where(Usuarios.id_usuario == id)).first()

        if not usuario:
            raise HTTPException("Usuario não encontrado")

        db.delete(usuario)
        db.commit()

    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Não é possível excluir este usuario, pois existem solicitações vincuradas a ele."
        )

def editarUsuario(id: int, usuarios: Usuarios, db: Session):
    try:
        usuario = db.get(Usuarios, id)

        if not usuario:
            raise HTTPException("Usuario não encontrado")

        usuario.cpf = usuarios.cpf
        usuario.nome = usuarios.nome
        usuario.email = usuarios.email
        usuario.status_usuario = usuarios.status_usuario
        usuario.perfil = usuarios.perfil

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return {
            f"O usuário {usuario.nome} editado com sucesso"
        }

    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError as e:
        raise ValueError("Verifique os dados") from e

def loginUsuario(email: str, senha: str, db: Session):

    try:
        usuario = db.exec(
            select(Usuarios).where(
                Usuarios.email == email
            )
        ).first()

        if not usuario:
            raise HTTPException(
                status_code=401,
                detail="E-mail ou senha incorretos"
            )

        if usuario.status_usuario != "Ativo":
            raise HTTPException(
                status_code=401,
                detail="Usuário bloqueado ou inativo"
            ) 

        senha_valida = verificar_password(
            senha,
            usuario.senha
        )

        if not senha_valida:
            raise HTTPException(
                status_code=401,
                detail="E-mail ou senha incorretos"
            )

        token = criar_token(
            email=usuario.email,
            expires_delta=timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario": {
                "id": usuario.id_usuario,
                "nome": usuario.nome,
                "email": usuario.email,
                "cpf": usuario.cpf,
                "perfil": usuario.perfil,
                "status": usuario.status_usuario,
                "data_cadastro": usuario.data_cadastro
            }
        }
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError as e:
        raise ValueError("Verifique os dados") from e