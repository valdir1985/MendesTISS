from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TabelaBase(BaseModel):
    nome: str
    codigo_tabela_ans: str
    ativo: Optional[bool] = True

class TabelaCreate(TabelaBase):
    pass

class TabelaUpdate(BaseModel):
    nome: Optional[str] = None
    codigo_tabela_ans: Optional[str] = None
    ativo: Optional[bool] = None

class TabelaResponse(TabelaBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
