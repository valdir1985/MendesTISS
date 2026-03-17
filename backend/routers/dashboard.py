from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.dashboard import DashboardResponse
from backend.services import dashboard_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario

router = APIRouter()

def get_clinica_id(x_clinica_id: Optional[int] = Header(None)):
    if not x_clinica_id:
        raise HTTPException(status_code=400, detail="Cabeçalho X-Clinica-Id é obrigatório para esta operação.")
    return x_clinica_id

@router.get("/resumo", response_model=DashboardResponse)
def obter_resumo_dashboard(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    clinica_id: int = Depends(get_clinica_id)
):
    """
    Retorna os principais KPIs e métricas financeiras da clínica ativa.
    """
    return dashboard_service.obter_dados_dashboard(db, clinica_id)
