from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.guia import GuiaCreate, GuiaResponse, GuiaStatusUpdate
from backend.services import guia_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario

router = APIRouter()

@router.post("/", response_model=GuiaResponse, status_code=status.HTTP_201_CREATED)
def criar_guia(
    guia: GuiaCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cria uma nova guia médica e todos os seus procedimentos associados de uma só vez.
    A guia é criada inicialmente com o status 'digitada'.
    """
    if not guia.procedimentos or len(guia.procedimentos) == 0:
        raise HTTPException(status_code=400, detail="A guia deve conter pelo menos um procedimento.")
        
    try:
        nova_guia = guia_service.create_guia(db=db, guia_in=guia)
        return nova_guia
    except Exception as e:
        # Idealmente, deve-se mapear erros específicos (ex: chave estrangeira não encontrada)
        raise HTTPException(status_code=400, detail=f"Erro ao criar guia: {str(e)}")

@router.get("/", response_model=List[GuiaResponse])
def listar_guias(
    skip: int = 0, 
    limit: int = 100,
    paciente_id: Optional[int] = Query(None, description="Filtrar guias por paciente"),
    status_guia: Optional[str] = Query(None, description="Filtrar por status (ex: digitada, em_lote)"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista todas as guias do sistema, com suporte a filtros básicos."""
    return guia_service.get_guias(db, skip=skip, limit=limit, paciente_id=paciente_id, status=status_guia)

@router.get("/{guia_id}", response_model=GuiaResponse)
def obter_guia(
    guia_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtém uma guia detalhada, incluindo todos os procedimentos executados."""
    db_guia = guia_service.get_guia(db, guia_id=guia_id)
    if db_guia is None:
        raise HTTPException(status_code=404, detail="Guia não encontrada.")
    return db_guia

@router.patch("/{guia_id}/status", response_model=GuiaResponse)
def alterar_status_guia(
    guia_id: int, 
    status_update: GuiaStatusUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Altera o status da guia (ex: de 'digitada' para 'em_lote').
    Esta rota será muito utilizada pela automação do Lote TISS.
    """
    db_guia = guia_service.update_guia_status(db, guia_id, status_update)
    if db_guia is None:
        raise HTTPException(status_code=404, detail="Guia não encontrada.")
    return db_guia
