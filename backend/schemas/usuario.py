from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Schema para criação de usuário
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    tipo_usuario: str = "colaborador"

# Schema para resposta (não inclui a senha)
class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    tipo_usuario: str
    ativo: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Schemas para o JWT
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None