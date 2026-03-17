from pydantic import BaseModel
from typing import Dict

class ResumoFinanceiro(BaseModel):
    total_faturado: float
    total_recebido: float
    total_glosado: float
    valor_a_receber: float

class DashboardResponse(BaseModel):
    financeiro: ResumoFinanceiro
    status_guias: Dict[str, int]
    status_lotes: Dict[str, int]
    glosas_por_recurso: Dict[str, int]
