from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError, IntegrityError
from entidades.models.solicitacao_emprestimo_model import SolicitacaoEmprestimo
from entidades.models.equipamento_model import Equipamento
from entidades.models.usuario_model import Usuarios
from fastapi import HTTPException

def cadastrarSolicitacao(solicitacao_data: SolicitacaoEmprestimo, db: Session):
    try:
        usuario = db.get(Usuarios, solicitacao_data.usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        equipamento = db.get(Equipamento, solicitacao_data.equipamento_id)

        if not equipamento:
            raise ValueError("Equipamento não encontrado")

        if equipamento.status_equipamento != equipamento.status_equipamento.DISPONIVEL:
            raise ValueError("Equipamento não disponível para empréstimo")

        if equipamento.quantidade is None or equipamento.quantidade <= 0:
            raise ValueError("Equipamento não disponível para empréstimo")

        db.add(solicitacao_data)
        db.commit()
        db.refresh(solicitacao_data)

        equipamento.quantidade -= 1

        if equipamento.quantidade == 0:
            equipamento.status_equipamento = equipamento.status_equipamento.INDISPONIVEL

        db.add(equipamento)
        db.commit()
        db.refresh(equipamento)

        return solicitacao_data

    except Exception as e:
        db.rollback()
        print("ERRO REAL:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    except IntegrityError as e:
        raise ValueError("Erro de integridade nos dados informados") from e


def deletarSolicitacao(id: int, solicitacoes: SolicitacaoEmprestimo, db: Session):

    try:
        solicitacao = db.exec(select(SolicitacaoEmprestimo).where(solicitacoes.id_solicitacao_emprestimo == id)).first()

        if not solicitacao:
            raise HTTPException(
                status_code=404,
                detail="Solicitação não encontrada"
            )

        db.delete(solicitacao)
        db.commit()
        return {
            "Solicitação deletada com sucesso"
        }

    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e


def listarSolicitacao(db: Session, usuario: Usuarios):

    try:

        if usuario.perfil not in ("Administrador", "Gestor"):
            statement = select(SolicitacaoEmprestimo).where(SolicitacaoEmprestimo.usuario_id == usuario.id_usuario)
        else:
            statement = select(SolicitacaoEmprestimo)

        solicitacao = db.exec(statement).all()

        if not solicitacao:
            raise HTTPException("Nenhuma solicitação encontarda")

        return solicitacao
    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e

    
def editarSolicitacao(id: int, solicitacoes: SolicitacaoEmprestimo, db: Session):

    try:
        solicitacao = db.get(SolicitacaoEmprestimo, id)

        if not solicitacao:
            raise HTTPException("Soliciação informada não existe")

        solicitacao.status_solicitacao = solicitacoes.status_solicitacao
        solicitacao.data_aprovacao = solicitacoes.data_aprovacao
        solicitacao.equipamento_id = solicitacoes.equipamento_id
        solicitacao.id_aprovador = solicitacoes.id_aprovador

        db.add(solicitacao)
        db.commit()
        db.refresh(solicitacao)

        return solicitacao
        
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError as e:
        raise ValueError("Erro de integridade nos dados informados") from e

def aprovarSolicitacao(id: int, solicitacoes: SolicitacaoEmprestimo, aprovador_solicitacao: Usuarios, db: Session):

    try:
        solicitacao = db.get(SolicitacaoEmprestimo, id)
        
        if not solicitacao:
            raise HTTPException("Solicitação não encontrado")
        
        solicitacao.status_solicitacao = solicitacoes.status_solicitacao
        solicitacao.id_aprovador = aprovador_solicitacao.id_usuario
    
        db.add(solicitacao)
        db.commit()
        db.refresh(solicitacao)
    
        return {
            f"Solicitação ID {solicitacao.id_solicitacao_emprestimo} alterada com sucesso"
        }
    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError as e:
        raise ValueError("Erro de integridade nos dados informados") from e
    