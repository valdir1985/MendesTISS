import string
import random
import psycopg2
from psycopg2 import sql
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models.clinica import Clinica
from backend.schemas.clinica import ClinicaCreate
from backend.config import settings

def gerar_senha_aleatoria(tamanho=12):
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(caracteres) for i in range(tamanho))

def criar_banco_dados_tenant(db_name: str, db_user: str, db_password: str):
    """Conecta diretamente no PostgreSQL para provisionar o banco e o usuário da nova clínica."""
    try:
        # Pega a URL do master mas isola os componentes usando psycopg2
        # Em produção, essas credenciais devem ser as de um superuser do PostgreSQL
        conn = psycopg2.connect(settings.DATABASE_URL)
        conn.autocommit = True
        cursor = conn.cursor()

        # Verifica se o usuário já existe
        cursor.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", (db_user,))
        if not cursor.fetchone():
            cursor.execute(
                sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(db_user)),
                [db_password]
            )

        # Verifica se o banco já existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname=%s", (db_name,))
        if not cursor.fetchone():
            cursor.execute(
                sql.SQL("CREATE DATABASE {} OWNER {}").format(
                    sql.Identifier(db_name),
                    sql.Identifier(db_user)
                )
            )
        
        cursor.close()
        conn.close()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao provisionar banco de dados da clínica: {str(e)}"
        )

def create_clinica(db: Session, clinica: ClinicaCreate):
    # Verifica se já existe CNPJ
    clinica_existente = db.query(Clinica).filter(Clinica.cnpj == clinica.cnpj).first()
    if clinica_existente:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado.")

    # Gera credenciais automáticas para a clínica
    sufixo = clinica.cnpj.replace(".", "").replace("/", "").replace("-", "")[:8]
    db_name = f"tenant_{sufixo}"
    db_user = f"user_{sufixo}"
    db_password = gerar_senha_aleatoria()

    # Provisiona o banco físico
    criar_banco_dados_tenant(db_name, db_user, db_password)

    # Registra no MASTER_DB
    nova_clinica = Clinica(
        nome=clinica.nome,
        cnpj=clinica.cnpj,
        database_name=db_name,
        database_host=clinica.database_host,
        database_port=clinica.database_port,
        database_user=db_user,
        database_password=db_password
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
