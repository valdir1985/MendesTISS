from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    
    # Estes campos serão Foreign Keys nas próximas etapas (Convênios e Planos)
    convenio_id = Column(Integer, nullable=True, index=True)
    plano_id = Column(Integer, nullable=True, index=True)
    
    numero_carteira = Column(String(50), nullable=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
