from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from backend.database import Base

class Clinica(Base):
    __tablename__ = "clinicas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    cnpj = Column(String(18), unique=True, index=True, nullable=False)
    
    # Credenciais do banco isolado da clínica
    database_name = Column(String(100), unique=True, nullable=False)
    database_host = Column(String(100), nullable=False, default="localhost")
    database_port = Column(Integer, nullable=False, default=5432)
    database_user = Column(String(100), nullable=False)
    database_password = Column(String(255), nullable=False)
    
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
