from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.plano import PlanoCreate, PlanoResponse, PlanoUpdate
from backend.services import plano_service, convenio_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario

router = APIRouter()

@router.post("/", response_model=PlanoResponse, status_code=status.HTTP_201_CREATED)
def criar_plano(
    plano: PlanoCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Regista um novo plano vinculado a um convênio existente."""
    
    # Valida se o convênio informado realmente existe
    convenio = convenio_service.get_convenio(db, convenio_id=plano.convenio_id)
    if not convenio:
        raise HTTPException(status_code=400, detail="O convênio especificado não existe.")

    return plano_service.create_plano(db=db, plano=plano)

@router.get("/", response_model=List[PlanoResponse])
def listar_planos(
    skip: int = 0, 
    limit: int = 100,
    convenio_id: Optional[int] = Query(None, description="Filtrar planos por ID do convênio"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status (ativo/inativo)"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista todos os planos, com opção de filtrar por operadora (convênio)."""
    return plano_service.get_planos(db, skip=skip, limit=limit, convenio_id=convenio_id, ativo=ativo)

@router.get("/{plano_id}", response_model=PlanoResponse)
def obter_plano(
    plano_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Busca os detalhes de um plano específico."""
    db_plano = plano_service.get_plano(db, plano_id=plano_id)
    if db_plano is None:
        raise HTTPException(status_code=404, detail="Plano não encontrado.")
    return db_plano

@router.put("/{plano_id}", response_model=PlanoResponse)
def atualizar_plano(
    plano_id: int, 
    plano_update: PlanoUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Atualiza os dados de um plano."""
    
    # Se estiver a atualizar o convenio_id, valida se o novo convênio existe
    if plano_update.convenio_id is not None:
        convenio = convenio_service.get_convenio(db, convenio_id=plano_update.convenio_id)
        if not convenio:
            raise HTTPException(status_code=400, detail="O novo convênio especificado não existe.")

    db_plano = plano_service.update_plano(db, plano_id, plano_update)
    if db_plano is None:
        raise HTTPException(status_code=404, detail="Plano não encontrado.")
    return db_plano

@router.delete("/{plano_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_plano(
    plano_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Remove um plano do sistema."""
    db_plano = plano_service.delete_plano(db, plano_id)
    if db_plano is None:
        raise HTTPException(status_code=404, detail="Plano não encontrado.")
    return None
