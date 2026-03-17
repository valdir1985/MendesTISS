from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RecursoGlosaCreate(BaseModel):
    glosa_id: int
    justificativa: str

class RecursoGlosaUpdate(BaseModel):
    status_recurso: Optional[str] = None
    justificativa: Optional[str] = None

class RecursoGlosaResponse(BaseModel):
    id: int
    glosa_id: int
    justificativa: str
    status_recurso: str
    data_recurso: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
