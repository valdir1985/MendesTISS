from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClinicaBase(BaseModel):
    nome: str
    cnpj: Optional[str] = None
    ativo: Optional[bool] = True

class ClinicaCreate(ClinicaBase):
    # Opcionais na criação inicial, podem ser preenchidos depois pelo sistema
    database_name: Optional[str] = None
    database_host: Optional[str] = None
    database_port: Optional[int] = None
    database_user: Optional[str] = None
    database_password: Optional[str] = None

class ClinicaUpdate(ClinicaBase):
    nome: Optional[str] = None
    database_name: Optional[str] = None
    database_host: Optional[str] = None
    database_port: Optional[int] = None
    database_user: Optional[str] = None
    database_password: Optional[str] = None

class ClinicaResponse(ClinicaBase):
    id: int
    database_name: Optional[str]
    database_host: Optional[str]
    database_port: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
