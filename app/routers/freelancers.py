from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/freelancers",
    tags=["Freelancer"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=schemas.FreelancerResponse, status_code=status.HTTP_201_CREATED
)
def create_freelancer(
    freelancer: schemas.FreelancerCreate, db: Session = Depends(get_db)
):
    # Verificar se email já existe
    db_user = (
        db.query(models.Usuario)
        .filter(models.Usuario.email == freelancer.email)
        .first()
    )
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")

    # Criar usuário
    new_user = models.Usuario(
        nome=freelancer.nome,
        email=freelancer.email,
        senha=freelancer.senha,  # Em produção, a senha deve ser hasheada
        telefone=freelancer.telefone,
        documento=freelancer.documento,
        tipo=freelancer.tipo,
        data_cadastro=date.today(),
    )
    db.add(new_user)
    db.flush()

    # Criar freelancer
    new_freelancer = models.Freelancer(
        id=new_user.id,
        especialidade=freelancer.especialidade,
        portfolio=freelancer.portfolio,
        avaliacao_media=0.0,
    )
    db.add(new_freelancer)
    db.commit()
    db.refresh(new_freelancer)

    # Construir resposta
    response = schemas.FreelancerResponse(
        id=new_freelancer.id,
        nome=new_user.nome,
        email=new_user.email,
        telefone=new_user.telefone,
        documento=new_user.documento,
        especialidade=new_freelancer.especialidade,
        portfolio=new_freelancer.portfolio,
        avaliacao_media=new_freelancer.avaliacao_media,
    )

    return response


@router.get("/", response_model=List[schemas.FreelancerResponse])
def get_freelancers_by_especialidade(
    especialidade: str = None, db: Session = Depends(get_db)
):
    query = db.query(models.Freelancer)

    # Se a especialidade for fornecida, aplica a busca fuzzy
    if especialidade:
        # Usa ILIKE para busca case-insensitive com padrão de correspondência
        query = query.filter(
            models.Freelancer.especialidade.ilike(f"%{especialidade}%")
        )

    freelancers = query.all()

    if not freelancers:
        raise HTTPException(status_code=404, detail="Nenhum freelancer encontrado")

    result = []
    for freelancer in freelancers:
        user = freelancer.usuario
        result.append(
            schemas.FreelancerResponse(
                id=freelancer.id,
                nome=user.nome,
                email=user.email,
                telefone=user.telefone,
                documento=user.documento,
                especialidade=freelancer.especialidade,
                portfolio=freelancer.portfolio,
                avaliacao_media=freelancer.avaliacao_media,
            )
        )

    return result


@router.put("/{id}", response_model=schemas.FreelancerResponse)
def update_freelancer(
    id: int, freelancer_update: schemas.FreelancerUpdate, db: Session = Depends(get_db)
):
    db_freelancer = (
        db.query(models.Freelancer).filter(models.Freelancer.id == id).first()
    )

    if not db_freelancer:
        raise HTTPException(status_code=404, detail="Freelancer não encontrado")

    # Atualizar campos
    for key, value in freelancer_update.dict(exclude_unset=True).items():
        setattr(db_freelancer, key, value)

    db.commit()
    db.refresh(db_freelancer)

    # Construir resposta
    user = db_freelancer.usuario
    response = schemas.FreelancerResponse(
        id=db_freelancer.id,
        nome=user.nome,
        email=user.email,
        telefone=user.telefone,
        documento=user.documento,
        especialidade=db_freelancer.especialidade,
        portfolio=db_freelancer.portfolio,
        avaliacao_media=db_freelancer.avaliacao_media,
    )

    return response
