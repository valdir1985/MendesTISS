from sqlalchemy.orm import Session
from backend.models.clinica import Clinica
from backend.schemas.clinica import ClinicaCreate, ClinicaUpdate

def get_clinica(db: Session, clinica_id: int):
    return db.query(Clinica).filter(Clinica.id == clinica_id).first()

def get_clinica_by_cnpj(db: Session, cnpj: str):
    return db.query(Clinica).filter(Clinica.cnpj == cnpj).first()

def get_clinicas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Clinica).offset(skip).limit(limit).all()

def create_clinica(db: Session, clinica: ClinicaCreate):
    db_clinica = Clinica(**clinica.model_dump())
    db.add(db_clinica)
    db.commit()
    db.refresh(db_clinica)
    return db_clinica

def update_clinica(db: Session, clinica_id: int, clinica_update: ClinicaUpdate):
    db_clinica = get_clinica(db, clinica_id)
    if not db_clinica:
        return None
    
    update_data = clinica_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_clinica, key, value)
        
    db.commit()
    db.refresh(db_clinica)
    return db_clinica

def delete_clinica(db: Session, clinica_id: int):
    db_clinica = get_clinica(db, clinica_id)
    if db_clinica:
        db.delete(db_clinica)
        db.commit()
    return db_clinica