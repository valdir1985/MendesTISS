from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.glosa import GlosaDetalheResponse, GlosaStatusUpdate
from backend.services import glosa_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario

router = APIRouter()

@router.get("/", response_model=List[GlosaDetalheResponse])
def listar_glosas(
    skip: int = 0, 
    limit: int = 100,
    status_recurso: Optional[str] = Query(None, description="Filtrar por status (ex: pendente, em_recurso)"),
    retorno_guia_id: Optional[int] = Query(None, description="Filtrar glosas de uma guia específica do retorno"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Lista todas as glosas registadas no sistema.
    Ideal para a equipa de faturação criar a sua 'Fila de Trabalho'.
    """
    return glosa_service.get_glosas(
        db, skip=skip, limit=limit, status_recurso=status_recurso, retorno_guia_id=retorno_guia_id
    )

@router.get("/{glosa_id}", response_model=GlosaDetalheResponse)
def obter_detalhes_glosa(
    glosa_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtém os detalhes de uma glosa específica."""
    db_glosa = glosa_service.get_glosa(db, glosa_id=glosa_id)
    if db_glosa is None:
        raise HTTPException(status_code=404, detail="Glosa não encontrada.")
    return db_glosa

@router.patch("/{glosa_id}/status", response_model=GlosaDetalheResponse)
def alterar_estado_glosa(
    glosa_id: int, 
    status_data: GlosaStatusUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Atualiza o estado de uma glosa. 
    Usado quando a equipa decide iniciar um recurso ou aceitar a glosa.
    """
    db_glosa = glosa_service.update_status_glosa(db, glosa_id, status_data)
    if db_glosa is None:
        raise HTTPException(status_code=404, detail="Glosa não encontrada.")
    return db_glosa

@router.get("/dashboard/resumo")
def resumo_glosas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Endpoint auxiliar para futuros gráficos e KPIs do sistema."""
    return glosa_service.get_estatisticas_glosas(db)
