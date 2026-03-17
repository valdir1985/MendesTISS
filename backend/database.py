import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Dict
from fastapi import HTTPException, status
from backend.config import settings

# Engine para o banco MASTER (onde ficam os usuários, clínicas, etc)
# CORREÇÃO: Usando settings.MASTER_DATABASE_URL conforme definido no seu config.py
engine = create_engine(
    settings.MASTER_DATABASE_URL,
    pool_pre_ping=True, # Garante que conexões caídas sejam descartadas
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Alias para manter compatibilidade com os serviços que chamam o banco master
MasterSessionLocal = SessionLocal 

Base = declarative_base()

# Cache de engines para os bancos das clínicas (Arquitetura Multi-tenant)
tenant_engines: Dict[str, create_engine] = {}

# Dependência padrão do FastAPI para injetar a sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependência explícita para o banco master (usada nas rotas de clínicas e auth)
def get_master_db():
    db = MasterSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_tenant_engine(clinica):
    """Cria ou recupera uma engine SQLAlchemy para o banco da clínica específica."""
    db_url = f"postgresql://{clinica.database_user}:{clinica.database_password}@{clinica.database_host}:{clinica.database_port}/{clinica.database_name}"
    
    if clinica.database_name not in tenant_engines:
        tenant_engine = create_engine(db_url, pool_pre_ping=True)
        tenant_engines[clinica.database_name] = tenant_engine
        
    return tenant_engines[clinica.database_name]

def get_tenant_db(clinica):
    """Gera uma sessão para o banco de dados da clínica informada."""
    tenant_engine = get_tenant_engine(clinica)
    TenantSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=tenant_engine)
    db = TenantSessionLocal()
    try:
        yield db
    finally:
        db.close()
