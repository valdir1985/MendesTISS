from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class RecursoGlosa(Base):
    __tablename__ = "recursos_glosa"

    id = Column(Integer, primary_key=True, index=True)
    
    # Relação 1:1 - Uma glosa tem um recurso
    glosa_id = Column(Integer, ForeignKey("glosas.id"), nullable=False, unique=True, index=True)
    
    justificativa = Column(Text, nullable=False)
    
    # Status interno do recurso: enviado, em_analise, acatado, negado
    status_recurso = Column(String(30), default="enviado")
    
    data_recurso = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamento com a Glosa
    glosa = relationship("Glosa")
