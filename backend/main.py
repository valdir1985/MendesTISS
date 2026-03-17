from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import settings
from backend.database import engine, Base

from backend.routers import (
    auth, clinicas, usuarios, pacientes, medicos, convenios, planos,
    tabelas, procedimentos, guias, lotes, tiss_engine, retornos, glosas, recursos, dashboard,
    frontend_pages
)

# Importar models (para criar tabelas)
from backend.models import (
    convite, paciente, medico, convenio, plano, tabela,
    procedimento, guia, lote, retorno, recurso_glosa
)

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS (ajusta se precisar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Frontend (HTML)
app.include_router(frontend_pages.router, tags=["Páginas Web"])

# API
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Autenticação"])
app.include_router(clinicas.router, prefix=f"{settings.API_V1_STR}/clinicas", tags=["Clínicas"])
app.include_router(usuarios.router, prefix=f"{settings.API_V1_STR}/usuarios", tags=["Usuários"])
app.include_router(pacientes.router, prefix=f"{settings.API_V1_STR}/pacientes", tags=["Pacientes"])
app.include_router(medicos.router, prefix=f"{settings.API_V1_STR}/medicos", tags=["Médicos"])
app.include_router(convenios.router, prefix=f"{settings.API_V1_STR}/convenios", tags=["Convênios"])
app.include_router(planos.router, prefix=f"{settings.API_V1_STR}/planos", tags=["Planos"])
app.include_router(tabelas.router, prefix=f"{settings.API_V1_STR}/tabelas", tags=["Tabelas"])
app.include_router(procedimentos.router, prefix=f"{settings.API_V1_STR}/procedimentos", tags=["Procedimentos"])
app.include_router(guias.router, prefix=f"{settings.API_V1_STR}/guias", tags=["Guias"])
app.include_router(lotes.router, prefix=f"{settings.API_V1_STR}/lotes", tags=["Lotes"])
app.include_router(tiss_engine.router, prefix=f"{settings.API_V1_STR}/tiss", tags=["TISS"])
app.include_router(retornos.router, prefix=f"{settings.API_V1_STR}/retornos", tags=["Retornos"])
app.include_router(glosas.router, prefix=f"{settings.API_V1_STR}/glosas", tags=["Glosas"])
app.include_router(recursos.router, prefix=f"{settings.API_V1_STR}/recursos", tags=["Recursos"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["Dashboard"])

@app.get("/")
def root():
    return {"message": "API MendesTiss rodando 🚀"}
