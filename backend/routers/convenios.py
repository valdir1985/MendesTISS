from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.convenio import ConvenioCreate, ConvenioResponse, ConvenioUpdate
from backend.services import convenio_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario

router = APIRouter()

@router.post("/", response_model=ConvenioResponse, status_code=status.HTTP_201_CREATED)
def criar_convenio(
    convenio: ConvenioCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Regista um novo convênio (Operadora). Valida a duplicação do Registro ANS."""
    
    # Validação do Registro ANS
    if convenio_service.get_convenio_by_registro_ans(db, registro_ans=convenio.registro_ans):
        raise HTTPException(status_code=400, detail="Já existe um convênio com este Registro ANS.")

    return convenio_service.create_convenio(db=db, convenio=convenio)

@router.get("/", response_model=List[ConvenioResponse])
def listar_convenios(
    skip: int = 0, 
    limit: int = 100,
    nome: Optional[str] = Query(None, description="Filtrar convênios por nome"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status (ativo/inativo)"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista todos os convênios configurados no sistema."""
    return convenio_service.get_convenios(db, skip=skip, limit=limit, nome=nome, ativo=ativo)

@router.get("/{convenio_id}", response_model=ConvenioResponse)
def obter_convenio(
    convenio_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Busca os detalhes de um convênio específico."""
    db_convenio = convenio_service.get_convenio(db, convenio_id=convenio_id)
    if db_convenio is None:
        raise HTTPException(status_code=404, detail="Convênio não encontrado.")
    return db_convenio

@router.put("/{convenio_id}", response_model=ConvenioResponse)
def atualizar_convenio(
    convenio_id: int, 
    convenio_update: ConvenioUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Atualiza os dados de um convênio."""
    # Opcional: Impedir atualização para um registro ANS que já pertence a outro convênio
    if convenio_update.registro_ans:
        existente = convenio_service.get_convenio_by_registro_ans(db, convenio_update.registro_ans)
        if existente and existente.id != convenio_id:
            raise HTTPException(status_code=400, detail="Este Registro ANS já está em uso por outro convênio.")

    db_convenio = convenio_service.update_convenio(db, convenio_id, convenio_update)
    if db_convenio is None:
        raise HTTPException(status_code=404, detail="Convênio não encontrado.")
    return db_convenio

@router.delete("/{convenio_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_convenio(
    convenio_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Remove um convênio do sistema."""
    db_convenio = convenio_service.delete_convenio(db, convenio_id)
    if db_convenio is None:
        raise HTTPException(status_code=404, detail="Convênio não encontrado.")
    return None
