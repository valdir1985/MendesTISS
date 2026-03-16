from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.medico import MedicoCreate, MedicoResponse, MedicoUpdate
from backend.services import medico_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario

router = APIRouter()

@router.post("/", response_model=MedicoResponse, status_code=status.HTTP_201_CREATED)
def criar_medico(
    medico: MedicoCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Regista um novo médico. Valida se o CRM+UF ou CPF já existem."""
    
    # Validação de CRM e UF duplicados
    if medico_service.get_medico_by_crm_uf(db, crm=medico.crm, uf_crm=medico.uf_crm):
        raise HTTPException(status_code=400, detail="Já existe um médico registado com este CRM e UF.")
        
    # Validação de CPF duplicado (se fornecido)
    if medico.cpf and medico_service.get_medico_by_cpf(db, cpf=medico.cpf):
        raise HTTPException(status_code=400, detail="Já existe um médico registado com este CPF.")

    return medico_service.create_medico(db=db, medico=medico)

@router.get("/", response_model=List[MedicoResponse])
def listar_medicos(
    skip: int = 0, 
    limit: int = 100,
    nome: Optional[str] = Query(None, description="Filtrar médicos por nome"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status (ativo/inativo)"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista os médicos, com opções de filtro por nome e estado."""
    return medico_service.get_medicos(db, skip=skip, limit=limit, nome=nome, ativo=ativo)

@router.get("/{medico_id}", response_model=MedicoResponse)
def obter_medico(
    medico_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Busca os detalhes de um médico específico."""
    db_medico = medico_service.get_medico(db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return db_medico

@router.put("/{medico_id}", response_model=MedicoResponse)
def atualizar_medico(
    medico_id: int, 
    medico_update: MedicoUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Atualiza os dados de um médico."""
    # Opcional: Adicionar lógicas de validação de duplicidade na atualização também
    db_medico = medico_service.update_medico(db, medico_id, medico_update)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return db_medico

@router.delete("/{medico_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_medico(
    medico_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Remove um médico do sistema."""
    db_medico = medico_service.delete_medico(db, medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return None
