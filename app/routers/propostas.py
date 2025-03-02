from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/propostas",
    tags=["Proposta de Serviço"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_proposta(
    proposta: schemas.PropostaServicoCreate, db: Session = Depends(get_db)
):
    # Verificar se evento existe
    evento = (
        db.query(models.Evento).filter(models.Evento.id == proposta.evento_id).first()
    )
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    # Verificar se freelancer existe
    freelancer = (
        db.query(models.Freelancer)
        .filter(models.Freelancer.id == proposta.freelancer_id)
        .first()
    )
    if not freelancer:
        raise HTTPException(status_code=404, detail="Freelancer não encontrado")

    # Criar proposta
    new_proposta = models.PropostaServico(
        evento_id=proposta.evento_id,
        freelancer_id=proposta.freelancer_id,
        data_proposta=proposta.data_proposta,
        status=proposta.status,
    )
    db.add(new_proposta)
    db.commit()

    return {"message": "Proposta enviada com sucesso"}


@router.patch("/{id}")
def update_proposta_status(
    id: int,
    proposta_update: schemas.PropostaServicoUpdate,
    db: Session = Depends(get_db),
):
    proposta = (
        db.query(models.PropostaServico).filter(models.PropostaServico.id == id).first()
    )

    if not proposta:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")

    # Validar status
    valid_status = ["Pendente", "Aceita", "Recusada", "Cancelada"]
    if proposta_update.status not in valid_status:
        raise HTTPException(
            status_code=400,
            detail=f"Status inválido. Valores permitidos: {', '.join(valid_status)}",
        )

    # Atualizar status
    proposta.status = proposta_update.status
    db.commit()

    return {"message": "Status da proposta atualizado com sucesso"}


@router.get("/freelancer/{id}", response_model=List[schemas.PropostaServicoResponse])
def get_propostas_by_freelancer(id: int, db: Session = Depends(get_db)):
    # Verificar se freelancer existe
    freelancer = db.query(models.Freelancer).filter(models.Freelancer.id == id).first()
    if not freelancer:
        raise HTTPException(status_code=404, detail="Freelancer não encontrado")

    # Buscar propostas
    propostas = (
        db.query(models.PropostaServico)
        .filter(models.PropostaServico.freelancer_id == id)
        .all()
    )

    if not propostas:
        raise HTTPException(
            status_code=404, detail="Nenhuma proposta encontrada para este freelancer"
        )

    return propostas
