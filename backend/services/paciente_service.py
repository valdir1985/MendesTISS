from sqlalchemy.orm import Session
from backend.models.paciente import Paciente
from backend.schemas.paciente import PacienteCreate

def create_paciente(db: Session, paciente: PacienteCreate, clinica_id: int):
    db_paciente = Paciente(
        nome=paciente.nome,
        numero_carteira=paciente.numero_carteira,
        clinica_id=clinica_id # Guarda a clínica automaticamente
    )
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

def get_pacientes(db: Session, clinica_id: int, skip: int = 0, limit: int = 100):
    # Retorna APENAS os pacientes da clínica ativa
    return db.query(Paciente).filter(Paciente.clinica_id == clinica_id).offset(skip).limit(limit).all()

def get_paciente(db: Session, paciente_id: int, clinica_id: int):
    # Garante que uma clínica não consegue ver o paciente de outra
    return db.query(Paciente).filter(Paciente.id == paciente_id, Paciente.clinica_id == clinica_id).first()
