from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from backend.database import Base

class ConviteUsuario(Base):
    __tablename__ = "convites_usuario"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), nullable=False, index=True)
    tipo_usuario = Column(String(20), nullable=False) # 'master' ou 'colaborador'
    
    # Gera um UUID automático e único para compor o link do convite
    token_convite = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    
    expira_em = Column(DateTime(timezone=True), nullable=False)
    utilizado = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
