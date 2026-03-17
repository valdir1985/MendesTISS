from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_master_db
from backend.schemas.clinica import ClinicaCreate, ClinicaResponse
from backend.services import clinica_service
from backend.models.usuario import Usuario
from backend.routers.auth import get_current_user

# CORREÇÃO: Sem prefixo aqui, pois o main.py já inclui o "/api/v1/clinicas"
router = APIRouter(tags=["Clínicas"])

@router.post("/", response_model=ClinicaResponse)
def criar_clinica(
    clinica: ClinicaCreate, 
    db: Session = Depends(get_master_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cadastra uma nova clínica e provisiona automaticamente um schema isolado
    no PostgreSQL/Supabase para ela. Apenas usuários master podem realizar esta ação.
    """
    if current_user.tipo_usuario != "master":
        raise HTTPException(status_code=403, detail="Apenas usuários master podem criar clínicas.")
        
    return clinica_service.create_clinica(db, clinica)

@router.get("/", response_model=List[ClinicaResponse])
def listar_clinicas(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_master_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista as clínicas cadastradas no sistema master."""
    return clinica_service.get_clinicas(db, skip=skip, limit=limit)

@router.get("/{clinica_id}", response_model=ClinicaResponse)
def obter_clinica(
    clinica_id: int, 
    db: Session = Depends(get_master_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Busca os detalhes de uma clínica pelo ID."""
    return clinica_service.get_clinica_by_id(db, clinica_id)
