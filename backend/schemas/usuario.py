from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Base Schema
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    tipo_usuario: str = "colaborador"
    clinica_id: Optional[int] = None

# Schema para Criação
class UsuarioCreate(UsuarioBase):
    senha: str

# Schema de Retorno (Response)
class UsuarioResponse(UsuarioBase):
    id: int
    ativo: bool
    email_verificado: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schemas para Autenticação / JWT
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
