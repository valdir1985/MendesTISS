from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

# --- SCHEMAS DE USUÁRIO ---
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    tipo_usuario: str = "colaborador"

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    tipo_usuario: Optional[str] = None
    ativo: Optional[bool] = None

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    tipo_usuario: str
    ativo: bool
    email_verificado: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- SCHEMAS DE CONVITE ---
class ConviteCreate(BaseModel):
    email: EmailStr
    tipo_usuario: str = "colaborador"

class ConviteResponse(BaseModel):
    id: int
    email: EmailStr
    tipo_usuario: str
    token_convite: UUID
    expira_em: datetime
    utilizado: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- SCHEMAS DE LOGIN ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
