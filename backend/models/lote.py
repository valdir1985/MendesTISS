from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class LoteTiss(Base):
    __tablename__ = "lotes_tiss"

    id = Column(Integer, primary_key=True, index=True)
    numero_lote = Column(String(50), unique=True, index=True, nullable=False)
    
    # O lote é sempre direcionado a uma operadora específica
    convenio_id = Column(Integer, ForeignKey("convenios.id"), nullable=False, index=True)
    
    status = Column(String(30), default="aberto") # aberto, enviado, processando, processado, erro
    valor_total = Column(Float, default=0.0)
    
    # --- NOVOS CAMPOS: CONTROLE DE ENVIO ---
    numero_protocolo = Column(String(100), nullable=True, index=True)
    data_envio = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamento com as guias contidas neste lote
    guias_rel = relationship("LoteGuia", back_populates="lote", cascade="all, delete-orphan")

class LoteGuia(Base):
    __tablename__ = "lote_guias"

    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("lotes_tiss.id"), nullable=False, index=True)
    
    # Uma guia só pode pertencer a um lote ativo por vez (unique=True evita duplicidade)
    guia_id = Column(Integer, ForeignKey("guias.id"), nullable=False, unique=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento reverso
    lote = relationship("LoteTiss", back_populates="guias_rel")
