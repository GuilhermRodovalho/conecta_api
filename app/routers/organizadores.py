from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/organizadores",
    tags=["Organizador"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=schemas.OrganizadorResponse, status_code=status.HTTP_201_CREATED
)
def create_organizador(
    organizador: schemas.OrganizadorCreate, db: Session = Depends(get_db)
):
    # Verificar se email já existe
    db_user = (
        db.query(models.Usuario)
        .filter(models.Usuario.email == organizador.email)
        .first()
    )
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")

    # Criar usuário
    new_user = models.Usuario(
        nome=organizador.nome,
        email=organizador.email,
        senha=organizador.senha,  # Em produção, a senha deve ser hasheada
        telefone=organizador.telefone,
        documento=organizador.documento,
        tipo=organizador.tipo,
        data_cadastro=date.today(),
    )
    db.add(new_user)
    db.flush()

    # Criar organizador
    new_organizador = models.Organizador(
        id=new_user.id, empresa_evento=organizador.empresa_evento, avaliacao_media=0.0
    )
    db.add(new_organizador)
    db.commit()
    db.refresh(new_organizador)

    # Construir resposta
    response = schemas.OrganizadorResponse(
        id=new_organizador.id,
        nome=new_user.nome,
        email=new_user.email,
        telefone=new_user.telefone,
        documento=new_user.documento,
        empresa_evento=new_organizador.empresa_evento,
        avaliacao_media=new_organizador.avaliacao_media,
    )

    return response
