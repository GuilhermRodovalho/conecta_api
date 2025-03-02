from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date


# Schemas base
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    documento: Optional[str] = None


class FreelancerBase(BaseModel):
    especialidade: str
    portfolio: Optional[str] = None


class OrganizadorBase(BaseModel):
    empresa_evento: str


class EventoBase(BaseModel):
    nome: str
    data_evento: date
    local: Optional[str] = None
    descricao: Optional[str] = None


class PropostaServicoBase(BaseModel):
    evento_id: int
    freelancer_id: int
    data_proposta: date
    status: str = "Pendente"


class AvaliacaoBase(BaseModel):
    avaliador_id: int
    avaliado_id: int
    nota: int = Field(..., ge=1, le=5)
    comentario: Optional[str] = None
    data_avaliacao: date


# Schemas para criação
class FreelancerCreate(UsuarioBase, FreelancerBase):
    senha: str
    tipo: str = "Freelancer"


class OrganizadorCreate(UsuarioBase, OrganizadorBase):
    senha: str
    tipo: str = "Organizador"


class EventoCreate(EventoBase):
    organizador_id: int


class PropostaServicoCreate(PropostaServicoBase):
    pass


class AvaliacaoCreate(AvaliacaoBase):
    pass


# Schemas para resposta
class FreelancerResponse(FreelancerBase):
    id: int
    nome: str
    email: EmailStr
    telefone: Optional[str]
    documento: Optional[str]
    avaliacao_media: Optional[float]

    class Config:
        orm_mode = True


class OrganizadorResponse(OrganizadorBase):
    id: int
    nome: str
    email: EmailStr
    telefone: Optional[str]
    documento: Optional[str]
    avaliacao_media: Optional[float]

    class Config:
        orm_mode = True


class EventoResponse(EventoBase):
    id: int
    organizador_id: int

    class Config:
        orm_mode = True


class PropostaServicoResponse(PropostaServicoBase):
    id: int

    class Config:
        orm_mode = True


class AvaliacaoResponse(AvaliacaoBase):
    id: int

    class Config:
        orm_mode = True


# Schemas para atualização
class FreelancerUpdate(BaseModel):
    especialidade: Optional[str] = None
    portfolio: Optional[str] = None

    class Config:
        orm_mode = True


class PropostaServicoUpdate(BaseModel):
    status: str

    class Config:
        orm_mode = True
