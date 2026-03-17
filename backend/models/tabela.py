from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from backend.database import Base

class TabelaProcedimento(Base):
    __tablename__ = "tabelas_procedimentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False) # Ex: "Tabela TISS", "CBHPM 5ª Edição"
    
    # Código oficial da tabela segundo a ANS (Ex: "22", "18", "98", "00")
    codigo_tabela_ans = Column(String(10), nullable=False, index=True)
    
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
