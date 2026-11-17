from entidades.models.usuario_model import UsuarioCadastro, Usuarios
from sqlmodel import Session, select
from fastapi import UploadFile
from services.password_hash import hash_password
from sqlalchemy.exc import OperationalError, IntegrityError
from services.password_hash import verificar_password
from auth.auth_login import criar_token
from pathlib import Path
from uuid import uuid4

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def inserirUsuarios(usuario: UsuarioCadastro, db: Session):
    try:
        user_existente_por_cpf = db.exec(
            select(Usuarios).where(
                Usuarios.cpf == usuario.cpf
            )
        ).first()

        if user_existente_por_cpf:
            raise ValueError("CPF duplicado")

        user_existente_por_email = db.exec(
            select(Usuarios).where(
                Usuarios.email == usuario.email
            )
        ).first()

        if user_existente_por_email:
            raise ValueError("Email duplicado")

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

    except ValueError:
        raise

    except OperationalError as e:
        db.rollback()
        raise ValueError("Falha na conexão com o banco de dados") from e

    except IntegrityError as e:
        db.rollback()
        raise ValueError("CPF ou e-mail já cadastrado") from e

def listarUsuario(db: Session):

    try:
        usuarios = db.exec(select(Usuarios)).all()

        if not usuarios:
            raise ValueError("Nenhum usuário encontrado")

        return usuarios
    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    
def deletarUsuario(id: int, db: Session):
    try:
        usuario = db.exec(select(Usuarios).where(Usuarios.id_usuario == id)).first()

        if not usuario:
            raise ValueError("Usuario não encontrado")

        db.delete(usuario)
        db.commit()

    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError:
        db.rollback()
        raise ValueError("Não é possível excluir este usuario, pois existem solicitações vincuradas a ele.")

def editarUsuario(id: int, usuarios: Usuarios, db: Session):
    try:
        usuario = db.get(Usuarios, id)

        if not usuario:
            raise ValueError("Usuario não encontrado")

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
            raise ValueError("E-mail ou senha incorretos")

        if usuario.status_usuario != usuario.status_usuario.ATIVO:
            raise ValueError("Usuário bloqueado ou inativo") 

        senha_valida = verificar_password(
            senha,
            usuario.senha
        )

        if not senha_valida:
            raise ValueError("E-mail ou senha incorretos")

        access_token = criar_token(
            email=usuario.email,
            perfil=usuario.perfil,
            tipo="access"
        )

        refresh_token = criar_token(
            email=usuario.email,
            perfil=usuario.perfil,
            tipo="refresh"
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id_usuario": usuario.id_usuario,
                "cpf": usuario.cpf,
                "nome": usuario.nome,
                "email": usuario.email,
                "status_usuario": usuario.status_usuario,
                "data_cadastro": usuario.data_cadastro,
                "perfil": usuario.perfil,
                "picture": usuario.picture
            }
        }
    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError as e:
        raise ValueError("Verifique os dados") from e

def updatPicture(db: Session, current_user: dict, picture: UploadFile):

    arquivo_salvo = None

    try:
        email = current_user.get("email")

        usuario = db.exec(
            select(Usuarios).where(Usuarios.email == email)
        ).first()

        if not usuario:
            raise ValueError("Usuário não encontrado")

        if not picture:
            raise ValueError("Nenhuma imagem enviada")

        # Validar formato da imagem
        extensao = Path(picture.filename).suffix.lower()

        extensoes_permitidas = [".jpg", ".jpeg", ".png", ".webp"]

        if extensao not in extensoes_permitidas:
            raise ValueError("Formato de imagem não permitido")

        if picture.content_type not in [
            "image/jpeg",
            "image/png",
            "image/webp"
        ]:
            raise ValueError("O arquivo enviado não é uma imagem válida")

        # Gerar nome único para evitar arquivos com nomes duplicados
        nome_arquivo = f"{uuid4().hex}{extensao}"

        caminho_arquivo = UPLOAD_DIR / nome_arquivo

        # Ler e salvar o arquivo
        conteudo = picture.file.read()

        if len(conteudo) > 5 * 1024 * 1024:
            raise ValueError("A imagem deve ter no máximo 5 MB")

        with open(caminho_arquivo, "wb") as arquivo:
            arquivo.write(conteudo)

        arquivo_salvo = caminho_arquivo

        # Guardar somente o caminho no banco
        foto_anterior = usuario.picture

        usuario.picture = f"/uploads/{nome_arquivo}"

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        # Remover foto anterior, se existir
        if foto_anterior:
            caminho_antigo = UPLOAD_DIR / Path(foto_anterior).name

            if caminho_antigo.is_file():
                caminho_antigo.unlink()

        return {
            "message": "Foto atualizada com sucesso",
            "picture_url": usuario.picture
        }

    except ValueError:
        db.rollback()

        if arquivo_salvo and arquivo_salvo.exists():
            arquivo_salvo.unlink()

        raise

    except OperationalError as e:
        db.rollback()

        if arquivo_salvo and arquivo_salvo.exists():
            arquivo_salvo.unlink()

        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e

    except Exception:
        db.rollback()

        if arquivo_salvo and arquivo_salvo.exists():
            arquivo_salvo.unlink()

        raise

def removePicture(db: Session, current_user: dict):

    try:
        email = current_user.get("email")

        usuario = db.exec(
            select(Usuarios).where(Usuarios.email == email)
        ).first()

        if not usuario:
            raise ValueError("Usuário não encontrado")

        if not usuario.picture:
            raise ValueError("Usuário não possui foto cadastrada")

        caminho_imagem = UPLOAD_DIR / Path(usuario.picture).name

        usuario.picture = None

        db.add(usuario)
        db.commit()

        if caminho_imagem.is_file():
            caminho_imagem.unlink()

        return {
            "message": "Foto removida com sucesso"
        }

    except OperationalError as e:
        db.rollback()

        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e