from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, status
from backend.models.clinica import Clinica
from backend.schemas.clinica import ClinicaCreate

def create_clinica(db: Session, clinica: ClinicaCreate):
    # Verifica se já existe CNPJ cadastrado
    clinica_existente = db.query(Clinica).filter(Clinica.cnpj == clinica.cnpj).first()
    if clinica_existente:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado no sistema.")

    # Cria um nome de schema único para a clínica baseado no CNPJ
    sufixo = clinica.cnpj.replace(".", "").replace("/", "").replace("-", "")[:8]
    schema_name = f"tenant_{sufixo}"

    # Provisiona o ambiente isolado da clínica no Supabase usando Schemas
    try:
        db.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao provisionar ambiente da clínica no Supabase: {str(e)}"
        )

    # Registra a clínica no banco Master
    nova_clinica = Clinica(
        nome=clinica.nome,
        cnpj=clinica.cnpj,
        database_name=schema_name,  # Salvamos o nome do Schema aqui!
        database_host="supabase",   # Host unificado
        database_port=5432,
        database_user="master_admin",
        database_password="-"
    )
    
    db.add(nova_clinica)
    db.commit()
    db.refresh(nova_clinica)
    
    return nova_clinica

def get_clinicas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Clinica).offset(skip).limit(limit).all()

def get_clinica_by_id(db: Session, clinica_id: int):
    clinica = db.query(Clinica).filter(Clinica.id == clinica_id).first()
    if not clinica:
        raise HTTPException(status_code=404, detail="Clínica não encontrada.")
    return clinica
