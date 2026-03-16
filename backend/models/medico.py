from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from backend.database import Base

class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    cpf = Column(String(14), unique=True, index=True, nullable=True)
    
    # Dados essenciais para o padrão TISS
    crm = Column(String(20), nullable=False, index=True)
    uf_crm = Column(String(2), nullable=False)
    cbo = Column(String(10), nullable=False) # Classificação Brasileira de Ocupações
    
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
