from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario
from backend.tiss.gerar_lote_xml import gerar_xml_tiss_lote

router = APIRouter()

@router.get("/lotes/{lote_id}/xml", response_class=Response)
def baixar_xml_lote(
    lote_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Gera e devolve o ficheiro XML de um Lote TISS, pronto para ser enviado à operadora.
    """
    try:
        xml_content = gerar_xml_tiss_lote(db, lote_id)
        
        # Devolve como um ficheiro XML descarregável
        return Response(
            content=xml_content, 
            media_type="application/xml",
            headers={"Content-Disposition": f"attachment; filename=Lote_TISS_{lote_id}.xml"}
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar XML: {str(e)}")
