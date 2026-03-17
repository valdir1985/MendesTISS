from sqlalchemy.orm import Session
from backend.models.retorno import Glosa, RetornoGuia, RetornoOperadora
from backend.schemas.glosa import GlosaStatusUpdate

def get_glosa(db: Session, glosa_id: int):
    return db.query(Glosa).filter(Glosa.id == glosa_id).first()

def get_glosas(db: Session, skip: int = 0, limit: int = 100, status_recurso: str = None, retorno_guia_id: int = None):
    query = db.query(Glosa)
    
    if status_recurso:
        query = query.filter(Glosa.status_recurso == status_recurso)
    if retorno_guia_id:
        query = query.filter(Glosa.retorno_guia_id == retorno_guia_id)
        
    return query.offset(skip).limit(limit).all()

def update_status_glosa(db: Session, glosa_id: int, status_data: GlosaStatusUpdate):
    db_glosa = get_glosa(db, glosa_id)
    if not db_glosa:
        return None
        
    db_glosa.status_recurso = status_data.status_recurso
    
    # Se houver um campo de observação no futuro, ele seria atualizado aqui
    # if hasattr(db_glosa, 'observacao_interna') and status_data.observacao_interna:
    #     db_glosa.observacao_interna = status_data.observacao_interna
        
    db.commit()
    db.refresh(db_glosa)
    return db_glosa

def get_estatisticas_glosas(db: Session):
    """Retorna um resumo financeiro e quantitativo das glosas para o Dashboard."""
    total_pendente = db.query(Glosa).filter(Glosa.status_recurso == "pendente").count()
    total_em_recurso = db.query(Glosa).filter(Glosa.status_recurso == "em_recurso").count()
    
    return {
        "pendentes": total_pendente,
        "em_recurso": total_em_recurso
    }
