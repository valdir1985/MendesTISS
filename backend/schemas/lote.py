from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- SCHEMA PARA CRIAR O LOTE ---
class LoteCreate(BaseModel):
    convenio_id: int
    guias_ids: List[int]

# --- SCHEMA PARA REGISTAR O ENVIO ---
class LoteMarcarEnviado(BaseModel):
    numero_protocolo: str

# --- SCHEMAS DE RESPOSTA ---
class LoteGuiaResponse(BaseModel):
    guia_id: int

    class Config:
        from_attributes = True

class LoteResponse(BaseModel):
    id: int
    numero_lote: str
    convenio_id: int
    status: str
    valor_total: float
    numero_protocolo: Optional[str] = None
    data_envio: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime]
    guias_rel: List[LoteGuiaResponse] = []

    class Config:
        from_attributes = True
