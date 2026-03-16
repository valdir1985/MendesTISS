from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from backend.database import Base

class Convenio(Base):
    __tablename__ = "convenios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    
    # Dados essenciais para a geração do XML TISS
    registro_ans = Column(String(20), unique=True, index=True, nullable=False)
    versao_tiss = Column(String(20), nullable=False, default="4.01.00")
    cnes = Column(String(20), nullable=True) # Cadastro Nacional de Estabelecimentos de Saúde (se exigido pela operadora)
    
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
