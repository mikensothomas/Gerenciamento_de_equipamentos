from entidades.models.usuario_model import Usuarios
from sqlmodel import Session, select
from fastapi import HTTPException

def inserirUsuarios(usuario: Usuarios, db = Session):
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
    
    inserir_usuarios = Usuarios.model_validate(usuario)
    db.add(inserir_usuarios)
    db.commit()
    db.refresh(inserir_usuarios)
    return inserir_usuarios
    