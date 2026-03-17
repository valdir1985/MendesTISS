from sqlalchemy.orm import Session
from backend.models.tabela import TabelaProcedimento
from backend.schemas.tabela import TabelaCreate, TabelaUpdate

def get_tabela(db: Session, tabela_id: int):
    return db.query(TabelaProcedimento).filter(TabelaProcedimento.id == tabela_id).first()

def get_tabela_by_codigo(db: Session, codigo_ans: str):
    # Retorna a primeira tabela encontrada com esse código (útil para validações)
    return db.query(TabelaProcedimento).filter(TabelaProcedimento.codigo_tabela_ans == codigo_ans).first()

def get_tabelas(db: Session, skip: int = 0, limit: int = 100, nome: str = None, ativo: bool = None):
    query = db.query(TabelaProcedimento)
    
    if nome:
        query = query.filter(TabelaProcedimento.nome.ilike(f"%{nome}%"))
    if ativo is not None:
        query = query.filter(TabelaProcedimento.ativo == ativo)
        
    return query.offset(skip).limit(limit).all()

def create_tabela(db: Session, tabela: TabelaCreate):
    db_tabela = TabelaProcedimento(**tabela.model_dump())
    db.add(db_tabela)
    db.commit()
    db.refresh(db_tabela)
    return db_tabela

def update_tabela(db: Session, tabela_id: int, tabela_update: TabelaUpdate):
    db_tabela = get_tabela(db, tabela_id)
    if not db_tabela:
        return None
    
    update_data = tabela_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tabela, key, value)
        
    db.commit()
    db.refresh(db_tabela)
    return db_tabela

def delete_tabela(db: Session, tabela_id: int):
    db_tabela = get_tabela(db, tabela_id)
    if db_tabela:
        db.delete(db_tabela)
        db.commit()
    return db_tabela
