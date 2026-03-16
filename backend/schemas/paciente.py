from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PacienteBase(BaseModel):
    nome: str
    convenio_id: Optional[int] = None
    plano_id: Optional[int] = None
    numero_carteira: Optional[str] = None

class PacienteCreate(PacienteBase):
    pass

class PacienteUpdate(BaseModel):
    nome: Optional[str] = None
    convenio_id: Optional[int] = None
    plano_id: Optional[int] = None
    numero_carteira: Optional[str] = None

class PacienteResponse(PacienteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
