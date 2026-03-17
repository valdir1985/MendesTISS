from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClinicaBase(BaseModel):
    nome: str
    cnpj: str
    database_host: str = "localhost"
    database_port: int = 5432

class ClinicaCreate(ClinicaBase):
    pass # Os dados sensíveis de DB serão gerados pelo backend no momento da criação

class ClinicaResponse(ClinicaBase):
    id: int
    database_name: str
    database_user: str
    ativo: bool
    created_at: datetime

    class Config:
        from_attributes = True
