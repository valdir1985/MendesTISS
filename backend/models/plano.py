from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.database import Base

class Plano(Base):
    __tablename__ = "planos_convenio"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    
    # Chave Estrangeira ligando o plano à operadora (convênio)
    convenio_id = Column(Integer, ForeignKey("convenios.id"), nullable=False, index=True)
    
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
