from sqlalchemy.orm import Session
from backend.models.procedimento import Procedimento
from backend.schemas.procedimento import ProcedimentoCreate, ProcedimentoUpdate

def get_procedimento(db: Session, procedimento_id: int):
    return db.query(Procedimento).filter(Procedimento.id == procedimento_id).first()

def get_procedimento_by_codigo_and_tabela(db: Session, codigo: str, tabela_id: int):
    return db.query(Procedimento).filter(
        Procedimento.codigo == codigo, 
        Procedimento.tabela_id == tabela_id
    ).first()

def get_procedimentos(db: Session, skip: int = 0, limit: int = 100, tabela_id: int = None, codigo: str = None, descricao: str = None, ativo: bool = None):
    query = db.query(Procedimento)
    
    if tabela_id is not None:
        query = query.filter(Procedimento.tabela_id == tabela_id)
    if codigo:
        query = query.filter(Procedimento.codigo.ilike(f"%{codigo}%"))
    if descricao:
        query = query.filter(Procedimento.descricao.ilike(f"%{descricao}%"))
    if ativo is not None:
        query = query.filter(Procedimento.ativo == ativo)
        
    return query.offset(skip).limit(limit).all()

def create_procedimento(db: Session, procedimento: ProcedimentoCreate):
    db_procedimento = Procedimento(**procedimento.model_dump())
    db.add(db_procedimento)
    db.commit()
    db.refresh(db_procedimento)
    return db_procedimento

def update_procedimento(db: Session, procedimento_id: int, procedimento_update: ProcedimentoUpdate):
    db_procedimento = get_procedimento(db, procedimento_id)
    if not db_procedimento:
        return None
    
    update_data = procedimento_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_procedimento, key, value)
        
    db.commit()
    db.refresh(db_procedimento)
    return db_procedimento

def delete_procedimento(db: Session, procedimento_id: int):
    db_procedimento = get_procedimento(db, procedimento_id)
    if db_procedimento:
        db.delete(db_procedimento)
        db.commit()
    return db_procedimento
