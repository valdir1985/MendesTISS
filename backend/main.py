from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database import engine, Base

# Importamos todos os routers construídos até agora
from backend.routers import auth, clinicas, usuarios, pacientes, medicos, convenios, planos, tabelas, procedimentos

# Importamos os models para garantir que o SQLAlchemy cria as tabelas no arranque
from backend.models import convite, paciente, medico, convenio, plano, tabela, procedimento

# Cria as tabelas na base de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API Master para gestão Multiclínicas e faturamento TISS",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registo das rotas (Endpoints)
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Autenticação"])
app.include_router(clinicas.router, prefix=f"{settings.API_V1_STR}/clinicas", tags=["Clínicas"])
app.include_router(usuarios.router, prefix=f"{settings.API_V1_STR}/usuarios", tags=["Usuários"])
app.include_router(pacientes.router, prefix=f"{settings.API_V1_STR}/pacientes", tags=["Pacientes"])
app.include_router(medicos.router, prefix=f"{settings.API_V1_STR}/medicos", tags=["Médicos"])
app.include_router(convenios.router, prefix=f"{settings.API_V1_STR}/convenios", tags=["Convênios"])
app.include_router(planos.router, prefix=f"{settings.API_V1_STR}/planos", tags=["Planos"])
app.include_router(tabelas.router, prefix=f"{settings.API_V1_STR}/tabelas", tags=["Tabelas de Domínio"])
app.include_router(procedimentos.router, prefix=f"{settings.API_V1_STR}/procedimentos", tags=["Procedimentos"]) # <-- NOVA ROTA

@app.get("/")
def root():
    return {"message": "Bem-vindo à API Master do sistema de faturamento."}
