from sqlalchemy.orm import Session
from backend.models.paciente import Paciente
from backend.schemas.paciente import PacienteCreate, PacienteUpdate

def get_paciente(db: Session, paciente_id: int):
    return db.query(Paciente).filter(Paciente.id == paciente_id).first()

def get_pacientes(db: Session, skip: int = 0, limit: int = 100, nome: str = None):
    query = db.query(Paciente)
    if nome:
        query = query.filter(Paciente.nome.ilike(f"%{nome}%"))
    return query.offset(skip).limit(limit).all()

def create_paciente(db: Session, paciente: PacienteCreate):
    db_paciente = Paciente(**paciente.model_dump())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

def update_paciente(db: Session, paciente_id: int, paciente_update: PacienteUpdate):
    db_paciente = get_paciente(db, paciente_id)
    if not db_paciente:
        return None
    
    update_data = paciente_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_paciente, key, value)
        
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

def delete_paciente(db: Session, paciente_id: int):
    db_paciente = get_paciente(db, paciente_id)
    if db_paciente:
        db.delete(db_paciente)
        db.commit()
    return db_paciente
