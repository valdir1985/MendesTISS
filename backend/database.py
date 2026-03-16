from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.config import settings

# Engine para o banco MASTER (onde ficam os usuários, clínicas, etc)
engine = create_engine(
    settings.MASTER_DATABASE_URL,
    pool_pre_ping=True, # Garante que conexões caídas sejam descartadas
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência do FastAPI para injetar a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()