from sqlalchemy.orm import Session
from backend.models.guia import Guia, GuiaProcedimento
from backend.schemas.guia import GuiaCreate, GuiaStatusUpdate

def get_guia(db: Session, guia_id: int):
    return db.query(Guia).filter(Guia.id == guia_id).first()

def get_guias(db: Session, skip: int = 0, limit: int = 100, paciente_id: int = None, status: str = None):
    query = db.query(Guia)
    if paciente_id:
        query = query.filter(Guia.paciente_id == paciente_id)
    if status:
        query = query.filter(Guia.status == status)
    return query.offset(skip).limit(limit).all()

def create_guia(db: Session, guia_in: GuiaCreate):
    # 1. Cria a entidade base da Guia
    db_guia = Guia(
        paciente_id=guia_in.paciente_id,
        medico_executante_id=guia_in.medico_executante_id,
        medico_solicitante_id=guia_in.medico_solicitante_id,
        convenio_id=guia_in.convenio_id,
        plano_id=guia_in.plano_id,
        tipo_guia=guia_in.tipo_guia,
        numero_guia_operadora=guia_in.numero_guia_operadora,
        data_atendimento=guia_in.data_atendimento,
        status="digitada", # Regra de negócio: toda guia nasce como digitada
        numero_guia_prestador=None # Aqui seria o local de aplicar a engine de "numerador_guias.py" no futuro
    )
    
    db.add(db_guia)
    db.flush() # Salva a guia para obter o ID gerado, mas ainda dentro da transação
    
    # 2. Insere os procedimentos e calcula o valor total
    valor_total_guia = 0.0
    
    for proc_in in guia_in.procedimentos:
        total_item = proc_in.quantidade * proc_in.valor_unitario
        valor_total_guia += total_item
        
        db_item = GuiaProcedimento(
            guia_id=db_guia.id,
            procedimento_id=proc_in.procedimento_id,
            quantidade=proc_in.quantidade,
            valor_unitario=proc_in.valor_unitario,
            valor_total=total_item
        )
        db.add(db_item)
        
    # 3. Atualiza o valor total da guia
    db_guia.valor_total = valor_total_guia
    
    # 4. Comita tudo de uma vez
    db.commit()
    db.refresh(db_guia)
    
    return db_guia

def update_guia_status(db: Session, guia_id: int, status_update: GuiaStatusUpdate):
    db_guia = get_guia(db, guia_id)
    if not db_guia:
        return None
        
    db_guia.status = status_update.status
    db.commit()
    db.refresh(db_guia)
    return db_guia
