from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.paciente import PacienteCreate, PacienteResponse, PacienteUpdate
from backend.services import paciente_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario

router = APIRouter()

# Função auxiliar para garantir que o Frontend enviou o ID da clínica
def get_clinica_id(x_clinica_id: Optional[int] = Header(None)):
    if not x_clinica_id:
        raise HTTPException(status_code=400, detail="Cabeçalho X-Clinica-Id é obrigatório para esta operação.")
    return x_clinica_id

@router.post("/", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
def criar_paciente(
    paciente: PacienteCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    clinica_id: int = Depends(get_clinica_id) # <-- Exige a Clínica
):
    """Regista um novo paciente vinculado à clínica ativa."""
    return paciente_service.create_paciente(db=db, paciente=paciente, clinica_id=clinica_id)

@router.get("/", response_model=List[PacienteResponse])
def listar_pacientes(
    skip: int = 0, 
    limit: int = 100,
    nome: Optional[str] = Query(None, description="Filtrar pacientes por nome"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    clinica_id: int = Depends(get_clinica_id) # <-- Exige a Clínica
):
    """Lista todos os pacientes da clínica ativa."""
    return paciente_service.get_pacientes(db, clinica_id=clinica_id, skip=skip, limit=limit, nome=nome)

@router.get("/{paciente_id}", response_model=PacienteResponse)
def obter_paciente(
    paciente_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    clinica_id: int = Depends(get_clinica_id) # <-- Exige a Clínica
):
    """Busca os detalhes de um paciente garantindo o escopo da clínica."""
    db_paciente = paciente_service.get_paciente(db, paciente_id=paciente_id, clinica_id=clinica_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado nesta clínica.")
    return db_paciente

@router.put("/{paciente_id}", response_model=PacienteResponse)
def atualizar_paciente(
    paciente_id: int, 
    paciente_update: PacienteUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    clinica_id: int = Depends(get_clinica_id) # <-- Exige a Clínica
):
    """Atualiza os dados de um paciente existente na clínica ativa."""
    db_paciente = paciente_service.update_paciente(db, paciente_id=paciente_id, paciente_update=paciente_update, clinica_id=clinica_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado nesta clínica.")
    return db_paciente

@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_paciente(
    paciente_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    clinica_id: int = Depends(get_clinica_id) # <-- Exige a Clínica
):
    """Remove um paciente do sistema respeitando o escopo da clínica."""
    db_paciente = paciente_service.delete_paciente(db, paciente_id=paciente_id, clinica_id=clinica_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado nesta clínica.")
    return None
