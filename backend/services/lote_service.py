from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from backend.models.lote import LoteTiss, LoteGuia
from backend.models.guia import Guia
from backend.schemas.lote import LoteCreate

def create_lote(db: Session, lote_in: LoteCreate):
    # 1. Busca todas as guias solicitadas
    guias = db.query(Guia).filter(Guia.id.in_(lote_in.guias_ids)).all()
    
    if len(guias) != len(lote_in.guias_ids):
        raise ValueError("Uma ou mais guias não foram encontradas na base de dados.")
        
    valor_total_lote = 0.0
    
    # 2. Validações de regra de negócio
    for guia in guias:
        if guia.convenio_id != lote_in.convenio_id:
            raise ValueError(f"A guia ID {guia.id} não pertence ao convênio especificado (ID {lote_in.convenio_id}).")
        
        if guia.status != "digitada":
            raise ValueError(f"A guia ID {guia.id} não pode ser incluída. Status atual: '{guia.status}'. Requerido: 'digitada'.")
            
        valor_total_lote += guia.valor_total

    # 3. Gera um número de lote único (Pode ser sequencial no futuro, usaremos UUID curto por agora)
    numero_lote_gerado = f"LT{datetime.now().strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"
    
    # 4. Cria o cabeçalho do Lote
    db_lote = LoteTiss(
        numero_lote=numero_lote_gerado,
        convenio_id=lote_in.convenio_id,
        status="aberto",
        valor_total=valor_total_lote
    )
    db.add(db_lote)
    db.flush() # Obtém o ID do lote gerado sem commitar a transação
    
    # 5. Vincula as guias ao lote e altera o status da Guia
    for guia in guias:
        db_lote_guia = LoteGuia(lote_id=db_lote.id, guia_id=guia.id)
        db.add(db_lote_guia)
        
        # REGRA TISS: A guia passa para 'em_lote'
        guia.status = "em_lote"
        
    # 6. Salva tudo de forma segura
    db.commit()
    db.refresh(db_lote)
    return db_lote

def get_lotes(db: Session, skip: int = 0, limit: int = 100, convenio_id: int = None, status: str = None):
    query = db.query(LoteTiss)
    if convenio_id is not None:
        query = query.filter(LoteTiss.convenio_id == convenio_id)
    if status:
        query = query.filter(LoteTiss.status == status)
    return query.offset(skip).limit(limit).all()

def get_lote(db: Session, lote_id: int):
    return db.query(LoteTiss).filter(LoteTiss.id == lote_id).first()
