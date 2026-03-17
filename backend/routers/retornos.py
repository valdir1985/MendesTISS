from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.retorno import RetornoOperadoraResponse
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario
from backend.tiss.parser_demonstrativo import importar_xml_retorno
from backend.models.retorno import RetornoOperadora

router = APIRouter()

@router.post("/importar", response_model=RetornoOperadoraResponse, status_code=status.HTTP_201_CREATED)
async def fazer_upload_retorno_xml(
    convenio_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Importa o arquivo XML de Demonstrativo de Pagamento (Retorno TISS).
    Processa os pagamentos, registra as glosas e atualiza o status das guias automaticamente.
    """
    if not file.filename.endswith(".xml"):
        raise HTTPException(status_code=400, detail="O arquivo deve ser um XML.")

    try:
        retorno_processado = await importar_xml_retorno(db, convenio_id, file)
        return retorno_processado
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar XML: {str(e)}")

@router.get("/", response_model=List[RetornoOperadoraResponse])
def listar_retornos(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista todos os históricos de retornos importados."""
    return db.query(RetornoOperadora).offset(skip).limit(limit).all()
