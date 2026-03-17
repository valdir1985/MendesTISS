from sqlalchemy.orm import Session
from backend.models.recurso_glosa import RecursoGlosa
from backend.models.retorno import Glosa
from backend.schemas.recurso_glosa import RecursoGlosaCreate, RecursoGlosaUpdate

def get_recurso(db: Session, recurso_id: int):
    return db.query(RecursoGlosa).filter(RecursoGlosa.id == recurso_id).first()

def get_recursos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RecursoGlosa).offset(skip).limit(limit).all()

def criar_recurso(db: Session, recurso_in: RecursoGlosaCreate):
    # 1. Valida se a glosa existe
    db_glosa = db.query(Glosa).filter(Glosa.id == recurso_in.glosa_id).first()
    if not db_glosa:
        raise ValueError("Glosa não encontrada no sistema.")
        
    # 2. Valida se já existe recurso para esta glosa
    existente = db.query(RecursoGlosa).filter(RecursoGlosa.glosa_id == recurso_in.glosa_id).first()
    if existente:
        raise ValueError("Já existe um recurso registado para esta glosa.")
        
    # 3. Cria o recurso
    db_recurso = RecursoGlosa(
        glosa_id=recurso_in.glosa_id,
        justificativa=recurso_in.justificativa
    )
    db.add(db_recurso)
    
    # 4. Atualiza o status da glosa para refletir que está a ser contestada
    db_glosa.status_recurso = "em_recurso"
    
    db.commit()
    db.refresh(db_recurso)
    return db_recurso

def atualizar_recurso(db: Session, recurso_id: int, recurso_update: RecursoGlosaUpdate):
    db_recurso = get_recurso(db, recurso_id)
    if not db_recurso:
        return None
        
    update_data = recurso_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_recurso, key, value)
        
    # Se o status do recurso for atualizado para 'acatado' ou 'negado', a glosa também deve refletir
    if recurso_update.status_recurso in ["acatado", "negado"]:
        db_glosa = db.query(Glosa).filter(Glosa.id == db_recurso.glosa_id).first()
        if db_glosa:
            # Mapeamento do status para a glosa
            db_glosa.status_recurso = f"recurso_{recurso_update.status_recurso}"
            
    db.commit()
    db.refresh(db_recurso)
    return db_recurso
