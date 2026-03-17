from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class RetornoOperadora(Base):
    __tablename__ = "retornos_operadora"

    id = Column(Integer, primary_key=True, index=True)
    convenio_id = Column(Integer, ForeignKey("convenios.id"), nullable=False, index=True)
    numero_protocolo_retorno = Column(String(100), index=True)
    
    data_recebimento = Column(Date, default=func.current_date())
    
    # Totais financeiros informados pela operadora no arquivo XML
    valor_total_informado = Column(Float, default=0.0)
    valor_total_pago = Column(Float, default=0.0)
    valor_total_glosado = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento com as guias deste retorno
    guias_retorno = relationship("RetornoGuia", back_populates="retorno", cascade="all, delete-orphan")

class RetornoGuia(Base):
    __tablename__ = "retorno_guias"

    id = Column(Integer, primary_key=True, index=True)
    retorno_id = Column(Integer, ForeignKey("retornos_operadora.id"), nullable=False, index=True)
    guia_id = Column(Integer, ForeignKey("guias.id"), nullable=False, index=True)
    
    status_pagamento = Column(String(30)) # paga, parcialmente_paga, glosada
    
    valor_informado = Column(Float, default=0.0)
    valor_pago = Column(Float, default=0.0)
    valor_glosado = Column(Float, default=0.0)

    retorno = relationship("RetornoOperadora", back_populates="guias_retorno")
    glosas = relationship("Glosa", back_populates="retorno_guia", cascade="all, delete-orphan")

class Glosa(Base):
    __tablename__ = "glosas"

    id = Column(Integer, primary_key=True, index=True)
    retorno_guia_id = Column(Integer, ForeignKey("retorno_guias.id"), nullable=False, index=True)
    
    codigo_glosa = Column(String(20), nullable=False)
    descricao_glosa = Column(String(500))
    valor_glosado = Column(Float, nullable=False)
    
    # pendente, em_recurso, recurso_aceito, recurso_negado
    status_recurso = Column(String(30), default="pendente") 

    retorno_guia = relationship("RetornoGuia", back_populates="glosas")
