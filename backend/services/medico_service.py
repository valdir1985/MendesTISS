from sqlalchemy.orm import Session
from backend.models.medico import Medico
from backend.schemas.medico import MedicoCreate, MedicoUpdate

def get_medico(db: Session, medico_id: int):
    return db.query(Medico).filter(Medico.id == medico_id).first()

def get_medico_by_crm_uf(db: Session, crm: str, uf_crm: str):
    return db.query(Medico).filter(Medico.crm == crm, Medico.uf_crm == uf_crm).first()

def get_medico_by_cpf(db: Session, cpf: str):
    return db.query(Medico).filter(Medico.cpf == cpf).first()

def get_medicos(db: Session, skip: int = 0, limit: int = 100, nome: str = None, ativo: bool = None):
    query = db.query(Medico)
    if nome:
        query = query.filter(Medico.nome.ilike(f"%{nome}%"))
    if ativo is not None:
        query = query.filter(Medico.ativo == ativo)
    return query.offset(skip).limit(limit).all()

def create_medico(db: Session, medico: MedicoCreate):
    db_medico = Medico(**medico.model_dump())
    db.add(db_medico)
    db.commit()
    db.refresh(db_medico)
    return db_medico

def update_medico(db: Session, medico_id: int, medico_update: MedicoUpdate):
    db_medico = get_medico(db, medico_id)
    if not db_medico:
        return None
    
    update_data = medico_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_medico, key, value)
        
    db.commit()
    db.refresh(db_medico)
    return db_medico

def delete_medico(db: Session, medico_id: int):
    db_medico = get_medico(db, medico_id)
    if db_medico:
        db.delete(db_medico)
        db.commit()
    return db_medico
