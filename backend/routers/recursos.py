from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.recurso_glosa import RecursoGlosaCreate, RecursoGlosaResponse, RecursoGlosaUpdate
from backend.services import recurso_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario
from backend.tiss.gerar_recurso_glosa import gerar_xml_recurso_tiss

router = APIRouter()

@router.post("/", response_model=RecursoGlosaResponse, status_code=status.HTTP_201_CREATED)
def elaborar_recurso(
    recurso: RecursoGlosaCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Cria a contestação (recurso) para uma glosa específica."""
    try:
        return recurso_service.criar_recurso(db=db, recurso_in=recurso)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.get("/", response_model=List[RecursoGlosaResponse])
def listar_recursos(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista todos os recursos elaborados pela clínica."""
    return recurso_service.get_recursos(db, skip=skip, limit=limit)

@router.put("/{recurso_id}", response_model=RecursoGlosaResponse)
def atualizar_status_recurso(
    recurso_id: int,
    recurso_update: RecursoGlosaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Atualiza o estado do recurso (ex: após a operadora responder se aceitou ou negou a contestação)."""
    db_recurso = recurso_service.atualizar_recurso(db, recurso_id, recurso_update)
    if db_recurso is None:
        raise HTTPException(status_code=404, detail="Recurso não encontrado.")
    return db_recurso

@router.get("/{recurso_id}/xml", response_class=Response)
def baixar_xml_recurso(
    recurso_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Gera o ficheiro XML do recurso para ser enviado à operadora."""
    try:
        xml_content = gerar_xml_recurso_tiss(db, recurso_id)
        
        return Response(
            content=xml_content, 
            media_type="application/xml",
            headers={"Content-Disposition": f"attachment; filename=Recurso_Glosa_{recurso_id}.xml"}
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar XML: {str(e)}")
