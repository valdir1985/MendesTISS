from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.guia import GuiaCreate, GuiaResponse, GuiaStatusUpdate
from backend.services import guia_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario

router = APIRouter()

# Função auxiliar para garantir o escopo multiclínicas
def get_clinica_id(x_clinica_id: Optional[int] = Header(None)):
    if not x_clinica_id:
        raise HTTPException(status_code=400, detail="Cabeçalho X-Clinica-Id é obrigatório para esta operação.")
    return x_clinica_id

@router.post("/", response_model=GuiaResponse, status_code=status.HTTP_201_CREATED)
def criar_guia(
    guia: GuiaCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    clinica_id: int = Depends(get_clinica_id) # <-- EXIGE A CLÍNICA
):
    """
    Cria uma nova guia médica e todos os seus procedimentos associados de uma só vez.
    A guia é criada inicialmente com o status 'digitada'.
    """
    if not guia.procedimentos or len(guia.procedimentos) == 0:
        raise HTTPException(status_code=400, detail="A guia deve conter pelo menos um procedimento.")
        
    try:
        nova_guia = guia_service.create_guia(db=db, guia_in=guia, clinica_id=clinica_id)
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
    current_user: Usuario = Depends(get_current_user),
    clinica_id: int = Depends(get_clinica_id) # <-- EXIGE A CLÍNICA
):
    """Lista todas as guias do sistema, com suporte a filtros básicos."""
    return guia_service.get_guias(db, clinica_id=clinica_id, skip=skip, limit=limit, paciente_id=paciente_id, status=status_guia)

@router.get("/{guia_id}", response_model=GuiaResponse)
def obter_guia(
    guia_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    clinica_id: int = Depends(get_clinica_id) # <-- EXIGE A CLÍNICA
):
    """Obtém uma guia detalhada, incluindo todos os procedimentos executados."""
    db_guia = guia_service.get_guia(db, guia_id=guia_id, clinica_id=clinica_id)
    if db_guia is None:
        raise HTTPException(status_code=404, detail="Guia não encontrada.")
    return db_guia

@router.patch("/{guia_id}/status", response_model=GuiaResponse)
def alterar_status_guia(
    guia_id: int, 
    status_update: GuiaStatusUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    clinica_id: int = Depends(get_clinica_id) # <-- EXIGE A CLÍNICA
):
    """
    Altera o status da guia (ex: de 'digitada' para 'em_lote').
    Esta rota será muito utilizada pela automação do Lote TISS.
    """
    db_guia = guia_service.update_guia_status(db, guia_id, status_update, clinica_id)
    if db_guia is None:
        raise HTTPException(status_code=404, detail="Guia não encontrada.")
    return db_guia
