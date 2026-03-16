from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MedicoBase(BaseModel):
    nome: str
    cpf: Optional[str] = None
    crm: str
    uf_crm: str
    cbo: str
    ativo: Optional[bool] = True

class MedicoCreate(MedicoBase):
    pass

class MedicoUpdate(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    crm: Optional[str] = None
    uf_crm: Optional[str] = None
    cbo: Optional[str] = None
    ativo: Optional[bool] = None

class MedicoResponse(MedicoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
