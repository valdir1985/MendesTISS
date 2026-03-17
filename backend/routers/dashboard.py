from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.dashboard import DashboardResponse
from backend.services import dashboard_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario

router = APIRouter()

@router.get("/resumo", response_model=DashboardResponse)
def obter_resumo_dashboard(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Retorna os principais KPIs e métricas financeiras do sistema.
    Calcula totais faturados, recebidos, glosados e a distribuição de status.
    """
    return dashboard_service.obter_dados_dashboard(db)
