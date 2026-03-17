from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_master_db
from backend.schemas.usuario import UsuarioCreate, UsuarioResponse
from backend.services import usuario_service
from backend.models.usuario import Usuario
from backend.routers.auth import get_current_user

# Sem prefixo aqui para evitar duplicação com o main.py
router = APIRouter(tags=["Usuários"])

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(
    usuario: UsuarioCreate, 
    db: Session = Depends(get_master_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cadastra um novo usuário no sistema. 
    Usuários master podem criar qualquer tipo de usuário para qualquer clínica.
    """
    if current_user.tipo_usuario != "master":
        raise HTTPException(status_code=403, detail="Apenas usuários master podem criar novos acessos no momento.")
        
    return usuario_service.create_usuario(db, usuario)

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    clinica_id: int = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_master_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista usuários. Se for master, pode ver de todas as clínicas ou filtrar por uma."""
    
    # Se o usuário não for master, ele só pode ver os usuários da própria clínica
    if current_user.tipo_usuario != "master":
        clinica_id = current_user.clinica_id
        
    return usuario_service.get_usuarios(db, clinica_id=clinica_id, skip=skip, limit=limit)
