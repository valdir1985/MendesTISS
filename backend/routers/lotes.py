from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.lote import LoteCreate, LoteResponse, LoteMarcarEnviado
from backend.services import lote_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario

router = APIRouter()

@router.post("/", response_model=LoteResponse, status_code=status.HTTP_201_CREATED)
def agrupar_guias_em_lote(
    lote_in: LoteCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Cria um novo Lote TISS contendo as guias especificadas."""
    if not lote_in.guias_ids or len(lote_in.guias_ids) == 0:
        raise HTTPException(status_code=400, detail="O lote deve conter pelo menos uma guia.")
        
    try:
        novo_lote = lote_service.create_lote(db=db, lote_in=lote_in)
        return novo_lote
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar lote: {str(e)}")

@router.get("/", response_model=List[LoteResponse])
def listar_lotes(
    skip: int = 0, 
    limit: int = 100,
    convenio_id: Optional[int] = Query(None, description="Filtrar por convênio"),
    status_lote: Optional[str] = Query(None, description="Filtrar por status do lote"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista os lotes gerados pela clínica."""
    return lote_service.get_lotes(db, skip=skip, limit=limit, convenio_id=convenio_id, status=status_lote)

@router.get("/{lote_id}", response_model=LoteResponse)
def obter_lote(
    lote_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Detalhes de um lote."""
    db_lote = lote_service.get_lote(db, lote_id=lote_id)
    if db_lote is None:
        raise HTTPException(status_code=404, detail="Lote não encontrado.")
    return db_lote

# --- NOVA ROTA DA ETAPA 13 ---
@router.patch("/{lote_id}/enviar", response_model=LoteResponse)
def registar_envio_lote(
    lote_id: int, 
    envio_data: LoteMarcarEnviado,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Regista que o lote foi enviado para a operadora.
    Salva o número do protocolo e altera as guias para o status 'enviada'.
    """
    try:
        db_lote = lote_service.marcar_lote_como_enviado(db, lote_id, envio_data)
        if db_lote is None:
            raise HTTPException(status_code=404, detail="Lote não encontrado.")
        return db_lote
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
