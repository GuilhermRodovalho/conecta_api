from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/avaliacoes",
    tags=["Avaliação"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_avaliacao(avaliacao: schemas.AvaliacaoCreate, db: Session = Depends(get_db)):
    # Verificar se avaliador existe
    avaliador = (
        db.query(models.Usuario)
        .filter(models.Usuario.id == avaliacao.avaliador_id)
        .first()
    )
    if not avaliador:
        raise HTTPException(status_code=404, detail="Avaliador não encontrado")

    # Verificar se avaliado existe
    avaliado = (
        db.query(models.Usuario)
        .filter(models.Usuario.id == avaliacao.avaliado_id)
        .first()
    )
    if not avaliado:
        raise HTTPException(status_code=404, detail="Avaliado não encontrado")

    # Criar avaliação
    new_avaliacao = models.Avaliacao(
        avaliador_id=avaliacao.avaliador_id,
        avaliado_id=avaliacao.avaliado_id,
        nota=avaliacao.nota,
        comentario=avaliacao.comentario,
        data_avaliacao=avaliacao.data_avaliacao,
    )
    db.add(new_avaliacao)
    db.commit()

    # Atualizar avaliação média
    # Para freelancer
    freelancer = (
        db.query(models.Freelancer)
        .filter(models.Freelancer.id == avaliacao.avaliado_id)
        .first()
    )
    if freelancer:
        avaliacoes = (
            db.query(models.Avaliacao)
            .filter(models.Avaliacao.avaliado_id == avaliacao.avaliado_id)
            .all()
        )
        soma = sum(a.nota for a in avaliacoes)
        freelancer.avaliacao_media = soma / len(avaliacoes)
        db.commit()

    # Para organizador
    organizador = (
        db.query(models.Organizador)
        .filter(models.Organizador.id == avaliacao.avaliado_id)
        .first()
    )
    if organizador:
        avaliacoes = (
            db.query(models.Avaliacao)
            .filter(models.Avaliacao.avaliado_id == avaliacao.avaliado_id)
            .all()
        )
        soma = sum(a.nota for a in avaliacoes)
        organizador.avaliacao_media = soma / len(avaliacoes)
        db.commit()

    return {"message": "Avaliação registrada com sucesso"}


@router.get("/", response_model=List[schemas.AvaliacaoResponse])
def get_avaliacoes_by_user(userId: int, db: Session = Depends(get_db)):
    # Verificar se usuário existe
    usuario = db.query(models.Usuario).filter(models.Usuario.id == userId).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Buscar avaliações
    avaliacoes = (
        db.query(models.Avaliacao).filter(models.Avaliacao.avaliado_id == userId).all()
    )

    if not avaliacoes:
        raise HTTPException(
            status_code=404, detail="Nenhuma avaliação encontrada para este usuário"
        )

    return avaliacoes
