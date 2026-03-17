from sqlalchemy.orm import Session
from backend.models.plano import Plano
from backend.schemas.plano import PlanoCreate, PlanoUpdate

def get_plano(db: Session, plano_id: int):
    return db.query(Plano).filter(Plano.id == plano_id).first()

def get_planos(db: Session, skip: int = 0, limit: int = 100, convenio_id: int = None, ativo: bool = None):
    query = db.query(Plano)
    
    if convenio_id is not None:
        query = query.filter(Plano.convenio_id == convenio_id)
    if ativo is not None:
        query = query.filter(Plano.ativo == ativo)
        
    return query.offset(skip).limit(limit).all()

def create_plano(db: Session, plano: PlanoCreate):
    db_plano = Plano(**plano.model_dump())
    db.add(db_plano)
    db.commit()
    db.refresh(db_plano)
    return db_plano

def update_plano(db: Session, plano_id: int, plano_update: PlanoUpdate):
    db_plano = get_plano(db, plano_id)
    if not db_plano:
        return None
    
    update_data = plano_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_plano, key, value)
        
    db.commit()
    db.refresh(db_plano)
    return db_plano

def delete_plano(db: Session, plano_id: int):
    db_plano = get_plano(db, plano_id)
    if db_plano:
        db.delete(db_plano)
        db.commit()
    return db_plano
