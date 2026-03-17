from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    tipo_usuario = Column(String(50), default="colaborador", nullable=False) # 'master' ou 'colaborador'
    
    # NOVO: Vínculo do usuário com uma clínica específica
    clinica_id = Column(Integer, ForeignKey("clinicas.id", ondelete="CASCADE"), nullable=True)

    ativo = Column(Boolean, default=True)
    email_verificado = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamento reverso (Opcional, mas útil para o SQLAlchemy)
    clinica = relationship("Clinica", backref="usuarios")
