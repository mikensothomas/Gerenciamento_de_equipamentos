from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError, IntegrityError

from entidades.models.perfil import Perfil


def cadastrarPerfil(
    perfil_data: Perfil,
    db: Session
):
    try:
        # Verifica se já existe um perfil com o mesmo nome
        perfil_existente = db.exec(
            select(Perfil).where(
                Perfil.nome == perfil_data.nome.strip()
            )
        ).first()

        if perfil_existente:
            raise ValueError("Já existe um perfil com esse nome")

        # Prepara os dados para cadastro
        dados = perfil_data.model_dump(
            exclude={"id", "data_criacao"}
        )

        dados["nome"] = dados["nome"].strip()
        dados["descricao"] = dados["descricao"].strip()

        perfil = Perfil(**dados)

        db.add(perfil)
        db.commit()
        db.refresh(perfil)

        return perfil

    except OperationalError as e:
        db.rollback()
        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e

    except IntegrityError as e:
        db.rollback()
        raise ValueError(
            "Verifique os dados informados"
        ) from e


def deletarPerfil(id: int, db: Session):

    try:
        perfil = db.get(Perfil, id)

        if not perfil:
            raise ValueError("Perfil não encontrado")

        db.delete(perfil)
        db.commit()

        return {
            "message": "Perfil deletado com sucesso!"
        }

    except OperationalError as e:
        db.rollback()
        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e


def listarPerfil(db: Session):

    try:
        perfis = db.exec(
            select(Perfil)
        ).all()

        return perfis

    except OperationalError as e:
        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e


def editarPerfil(
    id: int,
    perfilData: Perfil,
    db: Session
):
    try:
        perfil = db.get(Perfil, id)

        if not perfil:
            raise ValueError("Perfil não encontrado")

        # Verifica se outro perfil possui o mesmo nome
        perfil_existente = db.exec(
            select(Perfil).where(
                Perfil.nome == perfilData.nome.strip(),
                Perfil.id != id
            )
        ).first()

        if perfil_existente:
            raise ValueError(
                "Já existe outro perfil com esse nome"
            )

        perfil.nome = perfilData.nome.strip()
        perfil.descricao = perfilData.descricao.strip()
        perfil.status = perfilData.status

        db.add(perfil)
        db.commit()
        db.refresh(perfil)

        return perfil

    except OperationalError as e:
        db.rollback()
        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e

    except IntegrityError as e:
        db.rollback()
        raise ValueError(
            "Erro de integridade nos dados informados"
        ) from e