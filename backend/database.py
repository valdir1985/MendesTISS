import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Dict
from fastapi import HTTPException, status
from backend.config import settings

# Engine estática para o banco MASTER_DB
master_engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
MasterSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=master_engine)

Base = declarative_base()

# Cache de engines para os bancos das clínicas (evita criar múltiplas conexões para a mesma clínica)
tenant_engines: Dict[str, create_engine] = {}

def get_master_db():
    """Sessão para acessar tabelas de usuários, convites e controle de clínicas."""
    db = MasterSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_tenant_engine(clinica):
    """Cria ou recupera uma engine SQLAlchemy para o banco da clínica específica."""
    db_url = f"postgresql://{clinica.database_user}:{clinica.database_password}@{clinica.database_host}:{clinica.database_port}/{clinica.database_name}"
    
    if clinica.database_name not in tenant_engines:
        engine = create_engine(db_url, pool_pre_ping=True)
        tenant_engines[clinica.database_name] = engine
        
    return tenant_engines[clinica.database_name]

def get_tenant_db(clinica):
    """Gera uma sessão para o banco de dados da clínica informada."""
    engine = get_tenant_engine(clinica)
    TenantSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TenantSessionLocal()
    try:
        yield db
    finally:
        db.close()
