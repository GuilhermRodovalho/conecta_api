from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/eventos",
    tags=["Evento"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.EventoResponse])
def get_eventos(
    nome: Optional[str] = None,
    data_evento: Optional[date] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Evento)

    if nome:
        query = query.filter(models.Evento.nome.ilike(f"%{nome}%"))

    if data_evento:
        query = query.filter(models.Evento.data_evento == data_evento)

    eventos = query.all()

    if not eventos:
        raise HTTPException(status_code=404, detail="Nenhum evento encontrado")

    return eventos


@router.post(
    "/", response_model=schemas.EventoResponse, status_code=status.HTTP_201_CREATED
)
def create_evento(evento: schemas.EventoCreate, db: Session = Depends(get_db)):
    # Verificar se organizador existe
    organizador = (
        db.query(models.Organizador)
        .filter(models.Organizador.id == evento.organizador_id)
        .first()
    )
    if not organizador:
        raise HTTPException(status_code=404, detail="Organizador não encontrado")

    # Criar evento
    new_evento = models.Evento(
        organizador_id=evento.organizador_id,
        nome=evento.nome,
        data_evento=evento.data_evento,
        local=evento.local,
        descricao=evento.descricao,
    )
    db.add(new_evento)
    db.commit()
    db.refresh(new_evento)

    return new_evento
