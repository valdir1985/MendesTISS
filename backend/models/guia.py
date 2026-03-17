from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class Guia(Base):
    __tablename__ = "guias"

    id = Column(Integer, primary_key=True, index=True)
    
    # Relações com as entidades do sistema
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False, index=True)
    medico_executante_id = Column(Integer, ForeignKey("medicos.id"), nullable=False, index=True)
    medico_solicitante_id = Column(Integer, ForeignKey("medicos.id"), nullable=True) # Opcional, dependendo da guia
    convenio_id = Column(Integer, ForeignKey("convenios.id"), nullable=False, index=True)
    plano_id = Column(Integer, ForeignKey("planos_convenio.id"), nullable=False)
    
    # Dados específicos da Guia TISS
    tipo_guia = Column(String(50), nullable=False) # Ex: "Consulta", "SADT", "Honorario"
    numero_guia_operadora = Column(String(50), nullable=True, index=True) # Preenchido na autorização
    numero_guia_prestador = Column(String(50), nullable=True) # Gerado pelo nosso sistema
    
    data_emissao = Column(Date, nullable=False, default=func.current_date())
    data_atendimento = Column(Date, nullable=False)
    
    # Status da guia conforme a regra de negócio
    status = Column(String(30), nullable=False, default="digitada") 
    
    # Total financeiro da guia
    valor_total = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamento: Uma guia tem muitos procedimentos
    itens_procedimento = relationship("GuiaProcedimento", back_populates="guia", cascade="all, delete-orphan")


class GuiaProcedimento(Base):
    __tablename__ = "guia_procedimentos"

    id = Column(Integer, primary_key=True, index=True)
    guia_id = Column(Integer, ForeignKey("guias.id"), nullable=False, index=True)
    procedimento_id = Column(Integer, ForeignKey("procedimentos_tabela.id"), nullable=False)
    
    quantidade = Column(Integer, nullable=False, default=1)
    valor_unitario = Column(Float, nullable=False)
    valor_total = Column(Float, nullable=False) # quantidade * valor_unitario
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento reverso
    guia = relationship("Guia", back_populates="itens_procedimento")
