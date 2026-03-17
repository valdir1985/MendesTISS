from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProcedimentoBase(BaseModel):
    tabela_id: int
    codigo: str
    descricao: str
    valor: Optional[float] = None
    ativo: Optional[bool] = True

class ProcedimentoCreate(ProcedimentoBase):
    pass

class ProcedimentoUpdate(BaseModel):
    tabela_id: Optional[int] = None
    codigo: Optional[str] = None
    descricao: Optional[str] = None
    valor: Optional[float] = None
    ativo: Optional[bool] = None

class ProcedimentoResponse(ProcedimentoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
