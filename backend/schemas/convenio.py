from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ConvenioBase(BaseModel):
    nome: str
    registro_ans: str
    versao_tiss: str = "4.01.00"
    cnes: Optional[str] = None
    ativo: Optional[bool] = True

class ConvenioCreate(ConvenioBase):
    pass

class ConvenioUpdate(BaseModel):
    nome: Optional[str] = None
    registro_ans: Optional[str] = None
    versao_tiss: Optional[str] = None
    cnes: Optional[str] = None
    ativo: Optional[bool] = None

class ConvenioResponse(ConvenioBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
