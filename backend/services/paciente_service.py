from sqlalchemy.orm import Session
from backend.models.paciente import Paciente
from backend.schemas.paciente import PacienteCreate, PacienteUpdate

def get_paciente(db: Session, paciente_id: int, clinica_id: int):
    # Garante que a clínica só vê o seu próprio paciente
    return db.query(Paciente).filter(Paciente.id == paciente_id, Paciente.clinica_id == clinica_id).first()

def get_pacientes(db: Session, clinica_id: int, skip: int = 0, limit: int = 100, nome: str = None):
    # Filtra sempre pela clínica ativa
    query = db.query(Paciente).filter(Paciente.clinica_id == clinica_id)
    if nome:
        query = query.filter(Paciente.nome.ilike(f"%{nome}%"))
    return query.offset(skip).limit(limit).all()

def create_paciente(db: Session, paciente: PacienteCreate, clinica_id: int):
    # Injeta o clinica_id no momento da criação
    db_paciente = Paciente(
        nome=paciente.nome,
        numero_carteira=paciente.numero_carteira,
        clinica_id=clinica_id
    )
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

def update_paciente(db: Session, paciente_id: int, paciente_update: PacienteUpdate, clinica_id: int):
    # Busca verificando o clinica_id por segurança
    db_paciente = get_paciente(db, paciente_id, clinica_id)
    if not db_paciente:
        return None
    
    update_data = paciente_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_paciente, key, value)
        
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

def delete_paciente(db: Session, paciente_id: int, clinica_id: int):
    # Deleta apenas se pertencer à clínica
    db_paciente = get_paciente(db, paciente_id, clinica_id)
    if db_paciente:
        db.delete(db_paciente)
        db.commit()
    return db_paciente
