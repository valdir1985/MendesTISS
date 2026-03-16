from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database import engine, Base
# Importamos todos os routers construídos até agora
from backend.routers import auth, clinicas, usuarios, pacientes 
from backend.models import convite, paciente # Importar os models para criar as tabelas

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
app.include_router(pacientes.router, prefix=f"{settings.API_V1_STR}/pacientes", tags=["Pacientes"]) # <-- NOVA ROTA

@app.get("/")
def root():
    return {"message": "Bem-vindo à API Master do sistema de faturamento."}
