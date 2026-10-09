from entidades.models.usuario_model import UsuarioCadastro, Usuarios
from sqlmodel import Session, select
from fastapi import HTTPException
from services.password_hash import hash_password
from sqlalchemy.exc import OperationalError, IntegrityError
from services.password_hash import verificar_password
from datetime import timedelta
from auth.auth_login import ( criar_token, ACCESS_TOKEN_EXPIRE_MINUTES )

def inserirUsuarios(usuario: UsuarioCadastro, db: Session):
    try:
        user_existente_por_cpf = db.exec(
            select(Usuarios).where(
                Usuarios.cpf == usuario.cpf
            )
        ).first()

        if user_existente_por_cpf:
            raise HTTPException(
                status_code=400,
                detail="CPF duplicado"
            )

        user_existente_por_email = db.exec(
            select(Usuarios).where(
                Usuarios.email == usuario.email
            )
        ).first()

        if user_existente_por_email:
            raise HTTPException(
                status_code=400,
                detail="Email duplicado"
            )

        novo_usuario = Usuarios(
            cpf=usuario.cpf,
            nome=usuario.nome,
            email=usuario.email,
            senha=hash_password(usuario.senha),
            status_usuario=usuario.status_usuario,
            perfil=usuario.perfil
        )

        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        return {
            "message": "Cadastro feito com sucesso!"
        }

    except HTTPException:
        raise

    except OperationalError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Falha na conexão com o banco de dados"
        ) from e

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="CPF ou e-mail já cadastrado"
        ) from e

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

        if usuario.status_usuario != usuario.status_usuario.ATIVO:
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
            perfil=usuario.perfil,
            expires_delta=timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )
        
        return {
            "access_token": token,
            "token_type": "bearer",
        }
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError as e:
        raise ValueError("Verifique os dados") from e