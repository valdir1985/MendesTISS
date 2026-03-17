from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.procedimento import ProcedimentoCreate, ProcedimentoResponse, ProcedimentoUpdate
from backend.services import procedimento_service, tabela_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario

router = APIRouter()

@router.post("/", response_model=ProcedimentoResponse, status_code=status.HTTP_201_CREATED)
def criar_procedimento(
    procedimento: ProcedimentoCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Cria um novo procedimento associado a uma tabela de domínio."""
    
    # 1. Valida se a tabela de domínio existe
    tabela = tabela_service.get_tabela(db, tabela_id=procedimento.tabela_id)
    if not tabela:
        raise HTTPException(status_code=400, detail="A tabela de domínio especificada não existe.")
        
    # 2. Valida se já existe este código nesta mesma tabela
    existente = procedimento_service.get_procedimento_by_codigo_and_tabela(
        db, codigo=procedimento.codigo, tabela_id=procedimento.tabela_id
    )
    if existente:
        raise HTTPException(status_code=400, detail="Este código de procedimento já existe nesta tabela.")

    return procedimento_service.create_procedimento(db=db, procedimento=procedimento)

@router.get("/", response_model=List[ProcedimentoResponse])
def listar_procedimentos(
    skip: int = 0, 
    limit: int = 100,
    tabela_id: Optional[int] = Query(None, description="Filtrar por ID da tabela de domínio"),
    codigo: Optional[str] = Query(None, description="Filtrar por código do procedimento"),
    descricao: Optional[str] = Query(None, description="Filtrar por descrição"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista os procedimentos, com várias opções de filtro para facilitar a busca nas guias."""
    return procedimento_service.get_procedimentos(
        db, skip=skip, limit=limit, tabela_id=tabela_id, codigo=codigo, descricao=descricao, ativo=ativo
    )

@router.get("/{procedimento_id}", response_model=ProcedimentoResponse)
def obter_procedimento(
    procedimento_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Busca detalhes de um procedimento específico."""
    db_procedimento = procedimento_service.get_procedimento(db, procedimento_id=procedimento_id)
    if db_procedimento is None:
        raise HTTPException(status_code=404, detail="Procedimento não encontrado.")
    return db_procedimento

@router.put("/{procedimento_id}", response_model=ProcedimentoResponse)
def atualizar_procedimento(
    procedimento_id: int, 
    procedimento_update: ProcedimentoUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Atualiza as informações de um procedimento."""
    # Se mudar a tabela, tem que validar se ela existe
    if procedimento_update.tabela_id is not None:
        tabela = tabela_service.get_tabela(db, tabela_id=procedimento_update.tabela_id)
        if not tabela:
            raise HTTPException(status_code=400, detail="A nova tabela especificada não existe.")

    db_procedimento = procedimento_service.update_procedimento(db, procedimento_id, procedimento_update)
    if db_procedimento is None:
        raise HTTPException(status_code=404, detail="Procedimento não encontrado.")
    return db_procedimento

@router.delete("/{procedimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_procedimento(
    procedimento_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Remove um procedimento."""
    db_procedimento = procedimento_service.delete_procedimento(db, procedimento_id)
    if db_procedimento is None:
        raise HTTPException(status_code=404, detail="Procedimento não encontrado.")
    return None
