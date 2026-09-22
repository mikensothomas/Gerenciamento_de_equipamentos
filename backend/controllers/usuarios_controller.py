from entidades.models.usuario_model import Usuarios
from sqlmodel import Session, select
from fastapi import HTTPException
from services.password_hash import hash_password
from sqlalchemy.exc import OperationalError, IntegrityError

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