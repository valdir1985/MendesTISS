from pydantic import BaseModel
from typing import Optional

class GlosaStatusUpdate(BaseModel):
    # Estados previstos: pendente, em_recurso, recurso_aceito, recurso_negado, aceite_pela_clinica
    status_recurso: str
    
    # Num sistema avançado, a equipa pode querer adicionar uma nota interna
    observacao_interna: Optional[str] = None

class GlosaDetalheResponse(BaseModel):
    id: int
    retorno_guia_id: int
    codigo_glosa: str
    descricao_glosa: Optional[str]
    valor_glosado: float
    status_recurso: str

    class Config:
        from_attributes = True
