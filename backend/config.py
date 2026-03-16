from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "MendesTiss - API Master"
    API_V1_STR: str = "/api/v1"
    
    # JWT Settings
    SECRET_KEY: str = "SUA_CHAVE_SECRETA_MUITO_SEGURA_AQUI_MUDE_EM_PRODUCAO" # Em produção, use variáveis de ambiente
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 dias
    
    # Banco Master (Supabase)
    MASTER_DATABASE_URL: str = "postgresql://postgres.bkludjpifwgulwfpgsdw:MuAna2508%23%24@aws-1-sa-east-1.pooler.supabase.com:5432/postgres"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()