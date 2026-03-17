from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PacienteCreate(BaseModel):
    nome: str
    numero_carteira: Optional[str] = None
    # Não colocamos clinica_id aqui porque o utilizador não o digita, ele vem do sistema.

class PacienteResponse(BaseModel):
    id: int
    nome: str
    numero_carteira: Optional[str]
    clinica_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
