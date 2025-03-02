from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import freelancers, organizadores, eventos, propostas, avaliacoes

# Criar tabelas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Conecta",
    description="API para a plataforma Conecta de freelancers e organizadores de eventos",
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(freelancers.router)
app.include_router(organizadores.router)
app.include_router(eventos.router)
app.include_router(propostas.router)
app.include_router(avaliacoes.router)


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API Conecta"}
