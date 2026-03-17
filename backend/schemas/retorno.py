from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

class GlosaResponse(BaseModel):
    id: int
    codigo_glosa: str
    descricao_glosa: Optional[str]
    valor_glosado: float
    status_recurso: str

    class Config:
        from_attributes = True

class RetornoGuiaResponse(BaseModel):
    id: int
    guia_id: int
    status_pagamento: str
    valor_informado: float
    valor_pago: float
    valor_glosado: float
    glosas: List[GlosaResponse] = []

    class Config:
        from_attributes = True

class RetornoOperadoraResponse(BaseModel):
    id: int
    convenio_id: int
    numero_protocolo_retorno: Optional[str]
    data_recebimento: date
    valor_total_informado: float
    valor_total_pago: float
    valor_total_glosado: float
    created_at: datetime
    guias_retorno: List[RetornoGuiaResponse] = []

    class Config:
        from_attributes = True
