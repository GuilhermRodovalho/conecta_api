from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    Date,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from .database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)
    telefone = Column(String(50))
    documento = Column(String(50))  # CPF ou CNPJ
    tipo = Column(String(50), nullable=False)
    data_cadastro = Column(Date, nullable=False)

    __table_args__ = (CheckConstraint("tipo IN ('Freelancer', 'Organizador')"),)

    # Relações
    freelancer = relationship("Freelancer", back_populates="usuario", uselist=False)
    organizador = relationship("Organizador", back_populates="usuario", uselist=False)


class Profissao(Base):
    __tablename__ = "profissoes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)

    # Relações
    freelancers = relationship("Freelancer", back_populates="profissao")


class Freelancer(Base):
    __tablename__ = "freelancers"

    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    especialidade = Column(String(255))
    portfolio = Column(String(255))
    avaliacao_media = Column(Float)
    profissao_id = Column(Integer, ForeignKey("profissoes.id"))

    # Relações
    usuario = relationship("Usuario", back_populates="freelancer")
    profissao = relationship("Profissao", back_populates="freelancers")
    propostas = relationship("PropostaServico", back_populates="freelancer")


class Organizador(Base):
    __tablename__ = "organizadores"

    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    empresa_evento = Column(String(255))
    avaliacao_media = Column(Float)

    # Relações
    usuario = relationship("Usuario", back_populates="organizador")
    eventos = relationship("Evento", back_populates="organizador")


class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    organizador_id = Column(Integer, ForeignKey("organizadores.id"), nullable=False)
    nome = Column(String(255), nullable=False)
    data_evento = Column(Date, nullable=False)
    local = Column(String(255))
    descricao = Column(Text)

    # Relações
    organizador = relationship("Organizador", back_populates="eventos")
    propostas = relationship("PropostaServico", back_populates="evento")


class PropostaServico(Base):
    __tablename__ = "propostas_servico"

    id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    freelancer_id = Column(Integer, ForeignKey("freelancers.id"), nullable=False)
    data_proposta = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)

    __table_args__ = (
        CheckConstraint("status IN ('Pendente', 'Aceita', 'Recusada', 'Cancelada')"),
    )

    # Relações
    evento = relationship("Evento", back_populates="propostas")
    freelancer = relationship("Freelancer", back_populates="propostas")


class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    avaliador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    avaliado_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nota = Column(Integer)
    comentario = Column(Text)
    data_avaliacao = Column(Date, nullable=False)

    __table_args__ = (CheckConstraint("nota BETWEEN 1 AND 5"),)

    # Relações
    avaliador = relationship("Usuario", foreign_keys=[avaliador_id])
    avaliado = relationship("Usuario", foreign_keys=[avaliado_id])
