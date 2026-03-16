from sqlalchemy.orm import Session
from backend.models.convenio import Convenio
from backend.schemas.convenio import ConvenioCreate, ConvenioUpdate

def get_convenio(db: Session, convenio_id: int):
    return db.query(Convenio).filter(Convenio.id == convenio_id).first()

def get_convenio_by_registro_ans(db: Session, registro_ans: str):
    return db.query(Convenio).filter(Convenio.registro_ans == registro_ans).first()

def get_convenios(db: Session, skip: int = 0, limit: int = 100, nome: str = None, ativo: bool = None):
    query = db.query(Convenio)
    if nome:
        query = query.filter(Convenio.nome.ilike(f"%{nome}%"))
    if ativo is not None:
        query = query.filter(Convenio.ativo == ativo)
    return query.offset(skip).limit(limit).all()

def create_convenio(db: Session, convenio: ConvenioCreate):
    db_convenio = Convenio(**convenio.model_dump())
    db.add(db_convenio)
    db.commit()
    db.refresh(db_convenio)
    return db_convenio

def update_convenio(db: Session, convenio_id: int, convenio_update: ConvenioUpdate):
    db_convenio = get_convenio(db, convenio_id)
    if not db_convenio:
        return None
    
    update_data = convenio_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_convenio, key, value)
        
    db.commit()
    db.refresh(db_convenio)
    return db_convenio

def delete_convenio(db: Session, convenio_id: int):
    db_convenio = get_convenio(db, convenio_id)
    if db_convenio:
        db.delete(db_convenio)
        db.commit()
    return db_convenio
