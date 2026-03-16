from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from backend.database import Base

class Clinica(Base):
    __tablename__ = "clinicas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    cnpj = Column(String(20), unique=True, index=True, nullable=True)
    
    # Dados de conexão para o banco de dados isolado da clínica
    database_name = Column(String(100), nullable=True)
    database_host = Column(String(100), nullable=True)
    database_port = Column(Integer, nullable=True)
    database_user = Column(String(100), nullable=True)
    database_password = Column(String(200), nullable=True)
    
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
