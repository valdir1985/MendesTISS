from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.paciente import PacienteCreate, PacienteResponse, PacienteUpdate
from backend.services import paciente_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario

router = APIRouter()

@router.post("/", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
def criar_paciente(
    paciente: PacienteCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Regista um novo paciente no sistema da clínica."""
    return paciente_service.create_paciente(db=db, paciente=paciente)

@router.get("/", response_model=List[PacienteResponse])
def listar_pacientes(
    skip: int = 0, 
    limit: int = 100,
    nome: Optional[str] = Query(None, description="Filtrar pacientes por nome"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista todos os pacientes, com opção de pesquisa por nome e paginação."""
    return paciente_service.get_pacientes(db, skip=skip, limit=limit, nome=nome)

@router.get("/{paciente_id}", response_model=PacienteResponse)
def obter_paciente(
    paciente_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Busca os detalhes de um paciente específico pelo seu ID."""
    db_paciente = paciente_service.get_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return db_paciente

@router.put("/{paciente_id}", response_model=PacienteResponse)
def atualizar_paciente(
    paciente_id: int, 
    paciente_update: PacienteUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Atualiza os dados de um paciente existente."""
    db_paciente = paciente_service.update_paciente(db, paciente_id, paciente_update)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return db_paciente

@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_paciente(
    paciente_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Remove um paciente do sistema."""
    db_paciente = paciente_service.delete_paciente(db, paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return None
