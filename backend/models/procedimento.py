from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from backend.database import Base

class Procedimento(Base):
    __tablename__ = "procedimentos_tabela"

    id = Column(Integer, primary_key=True, index=True)
    
    # Relação com a tabela de domínio (ex: Tabela 22, CBHPM)
    tabela_id = Column(Integer, ForeignKey("tabelas_procedimentos.id"), nullable=False, index=True)
    
    # Código oficial (ex: 10101012 para Consulta em Consultório)
    codigo = Column(String(20), nullable=False, index=True)
    descricao = Column(String(500), nullable=False)
    
    # Valor financeiro padrão do procedimento (opcional, pode variar por convênio futuramente)
    valor = Column(Float, nullable=True)
    
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
