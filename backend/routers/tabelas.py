from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.tabela import TabelaCreate, TabelaResponse, TabelaUpdate
from backend.services import tabela_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario

router = APIRouter()

@router.post("/", response_model=TabelaResponse, status_code=status.HTTP_201_CREATED)
def criar_tabela(
    tabela: TabelaCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Cria o registo de uma nova tabela de domínio (ex: Tabela 22, CBHPM)."""
    return tabela_service.create_tabela(db=db, tabela=tabela)

@router.get("/", response_model=List[TabelaResponse])
def listar_tabelas(
    skip: int = 0, 
    limit: int = 100,
    nome: Optional[str] = Query(None, description="Filtrar por nome da tabela"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista as tabelas configuradas no sistema."""
    return tabela_service.get_tabelas(db, skip=skip, limit=limit, nome=nome, ativo=ativo)

@router.get("/{tabela_id}", response_model=TabelaResponse)
def obter_tabela(
    tabela_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Busca detalhes de uma tabela específica."""
    db_tabela = tabela_service.get_tabela(db, tabela_id=tabela_id)
    if db_tabela is None:
        raise HTTPException(status_code=404, detail="Tabela não encontrada.")
    return db_tabela

@router.put("/{tabela_id}", response_model=TabelaResponse)
def atualizar_tabela(
    tabela_id: int, 
    tabela_update: TabelaUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Atualiza as informações de uma tabela."""
    db_tabela = tabela_service.update_tabela(db, tabela_id, tabela_update)
    if db_tabela is None:
        raise HTTPException(status_code=404, detail="Tabela não encontrada.")
    return db_tabela

@router.delete("/{tabela_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_tabela(
    tabela_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Remove uma tabela do sistema (Cuidado com a integridade referencial futura)."""
    db_tabela = tabela_service.delete_tabela(db, tabela_id)
    if db_tabela is None:
        raise HTTPException(status_code=404, detail="Tabela não encontrada.")
    return None
