from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.config import settings

# Engine principal apontando para o seu Supabase (MASTER_DATABASE_URL)
engine = create_engine(
    settings.MASTER_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_master_db():
    """Acessa o banco master (onde ficam as tabelas de controle no schema public)."""
    db = SessionLocal()
    try:
        # Garante que as rotas master olhem para o schema principal
        db.execute(text("SET search_path TO public"))
        yield db
    finally:
        db.close()

def get_tenant_db(clinica):
    """
    MÁGICA DO MULTI-TENANT NO SUPABASE:
    Isola os dados da clínica alterando o schema (search_path) da sessão atual.
    Nenhuma clínica consegue ver os dados da outra.
    """
    db = SessionLocal()
    try:
        # Muda o foco do banco apenas para o "cercadinho" (schema) desta clínica
        db.execute(text(f"SET search_path TO {clinica.database_name}"))
        yield db
    finally:
        # Devolve o foco para o public ao encerrar a requisição por segurança
        db.execute(text("SET search_path TO public"))
        db.close()
