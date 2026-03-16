from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.clinica import ClinicaCreate, ClinicaResponse, ClinicaUpdate
from backend.services import clinica_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario

router = APIRouter()

@router.post("/", response_model=ClinicaResponse, status_code=status.HTTP_201_CREATED)
def create_clinica(
    clinica: ClinicaCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Cria uma nova clínica. Requer usuário autenticado."""
    if clinica.cnpj:
        db_clinica = clinica_service.get_clinica_by_cnpj(db, cnpj=clinica.cnpj)
        if db_clinica:
            raise HTTPException(status_code=400, detail="CNPJ já cadastrado no sistema.")
    return clinica_service.create_clinica(db=db, clinica=clinica)

@router.get("/", response_model=List[ClinicaResponse])
def read_clinicas(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista todas as clínicas."""
    return clinica_service.get_clinicas(db, skip=skip, limit=limit)

@router.get("/{clinica_id}", response_model=ClinicaResponse)
def read_clinica(
    clinica_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Busca uma clínica específica pelo ID."""
    db_clinica = clinica_service.get_clinica(db, clinica_id=clinica_id)
    if db_clinica is None:
        raise HTTPException(status_code=404, detail="Clínica não encontrada")
    return db_clinica

@router.put("/{clinica_id}", response_model=ClinicaResponse)
def update_clinica(
    clinica_id: int, 
    clinica_update: ClinicaUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Atualiza os dados de uma clínica."""
    db_clinica = clinica_service.update_clinica(db, clinica_id, clinica_update)
    if db_clinica is None:
        raise HTTPException(status_code=404, detail="Clínica não encontrada")
    return db_clinica