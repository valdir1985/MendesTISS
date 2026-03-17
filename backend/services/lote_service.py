from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from backend.models.lote import LoteTiss, LoteGuia
from backend.models.guia import Guia
from backend.schemas.lote import LoteCreate, LoteMarcarEnviado

def create_lote(db: Session, lote_in: LoteCreate, clinica_id: int):
    # Filtra as guias garantindo que pertencem à clínica ativa
    guias = db.query(Guia).filter(Guia.id.in_(lote_in.guias_ids), Guia.clinica_id == clinica_id).all()
    
    if len(guias) != len(lote_in.guias_ids):
        raise ValueError("Uma ou mais guias não foram encontradas na base de dados desta clínica.")
        
    valor_total_lote = 0.0
    
    for guia in guias:
        if guia.convenio_id != lote_in.convenio_id:
            raise ValueError(f"A guia ID {guia.id} não pertence ao convênio especificado (ID {lote_in.convenio_id}).")
        
        if guia.status != "digitada":
            raise ValueError(f"A guia ID {guia.id} não pode ser incluída. Status atual: '{guia.status}'.")
            
        valor_total_lote += guia.valor_total

    numero_lote_gerado = f"LT{datetime.now().strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"
    
    db_lote = LoteTiss(
        numero_lote=numero_lote_gerado,
        clinica_id=clinica_id, # <-- INJETADO AQUI
        convenio_id=lote_in.convenio_id,
        status="aberto",
        valor_total=valor_total_lote
    )
    db.add(db_lote)
    db.flush()
    
    for guia in guias:
        db_lote_guia = LoteGuia(lote_id=db_lote.id, guia_id=guia.id)
        db.add(db_lote_guia)
        guia.status = "em_lote"
        
    db.commit()
    db.refresh(db_lote)
    return db_lote

def get_lotes(db: Session, clinica_id: int, skip: int = 0, limit: int = 100, convenio_id: int = None, status: str = None):
    # Filtra os lotes da clínica
    query = db.query(LoteTiss).filter(LoteTiss.clinica_id == clinica_id)
    if convenio_id is not None:
        query = query.filter(LoteTiss.convenio_id == convenio_id)
    if status:
        query = query.filter(LoteTiss.status == status)
    return query.offset(skip).limit(limit).all()

def get_lote(db: Session, lote_id: int, clinica_id: int):
    # Busca o lote validando a clínica
    return db.query(LoteTiss).filter(LoteTiss.id == lote_id, LoteTiss.clinica_id == clinica_id).first()

# --- NOVA FUNÇÃO DA ETAPA 13 ---
def marcar_lote_como_enviado(db: Session, lote_id: int, envio_data: LoteMarcarEnviado, clinica_id: int):
    db_lote = get_lote(db, lote_id, clinica_id)
    if not db_lote:
        return None
        
    if db_lote.status != "aberto":
        raise ValueError(f"O lote não pode ser enviado. Status atual: {db_lote.status}")

    # 1. Atualiza os dados do Lote
    db_lote.status = "enviado"
    db_lote.numero_protocolo = envio_data.numero_protocolo
    db_lote.data_envio = datetime.now()
    
    # 2. Busca as guias vinculadas a este lote
    lote_guias = db.query(LoteGuia).filter(LoteGuia.lote_id == lote_id).all()
    guias_ids = [lg.guia_id for lg in lote_guias]
    
    # 3. Atualiza o status de todas as guias garantindo a clínica
    guias = db.query(Guia).filter(Guia.id.in_(guias_ids), Guia.clinica_id == clinica_id).all()
    for guia in guias:
        guia.status = "enviada"
        
    db.commit()
    db.refresh(db_lote)
    return db_lote
