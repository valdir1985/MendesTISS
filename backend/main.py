from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database import engine, Base
from backend.routers import auth, clinicas

# Cria as tabelas no banco de dados (Idealmente usar Alembic depois)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API Master para gestão Multiclínicas e faturamento TISS",
    version="1.0.0"
)

# Configuração de CORS para permitir que o Frontend acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Mude para as URLs do seu frontend em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Autenticação"])
app.include_router(clinicas.router, prefix=f"{settings.API_V1_STR}/clinicas", tags=["Clínicas"])

@app.get("/")
def root():
    return {"message": "Bem-vindo à API Master do sistema de faturamento."}
