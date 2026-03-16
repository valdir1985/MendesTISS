from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PlanoBase(BaseModel):
    nome: str
    convenio_id: int
    ativo: Optional[bool] = True

class PlanoCreate(PlanoBase):
    pass

class PlanoUpdate(BaseModel):
    nome: Optional[str] = None
    convenio_id: Optional[int] = None
    ativo: Optional[bool] = None

class PlanoResponse(PlanoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
