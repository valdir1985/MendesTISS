from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.usuario import UsuarioResponse, UsuarioUpdate, ConviteCreate, ConviteResponse
from backend.services import usuario_service
from backend.routers.auth import get_current_user
from backend.models.usuario import Usuario

router = APIRouter()

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista todos os usuários do sistema Master. Restrito a administradores."""
    if current_user.tipo_usuario != "master":
        raise HTTPException(status_code=403, detail="Apenas usuários master podem listar a equipe.")
    return usuario_service.get_usuarios(db, skip=skip, limit=limit)

@router.put("/{user_id}", response_model=UsuarioResponse)
def atualizar_usuario(
    user_id: int, 
    user_update: UsuarioUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Atualiza os dados de um usuário (ex: desativar acesso, mudar permissão)."""
    # Usuário só pode editar a si mesmo, a menos que seja master
    if current_user.tipo_usuario != "master" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Sem permissão para alterar este usuário.")
    
    db_user = usuario_service.update_usuario(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

@router.post("/convites", response_model=ConviteResponse, status_code=status.HTTP_201_CREATED)
def enviar_convite(
    convite: ConviteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Gera um link/token de convite para cadastrar um novo usuário na plataforma."""
    if current_user.tipo_usuario != "master":
        raise HTTPException(status_code=403, detail="Apenas administradores podem enviar convites.")
    return usuario_service.criar_convite(db, convite)
