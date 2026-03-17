from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models.usuario import Usuario
from backend.schemas.usuario import UsuarioCreate
from backend.core.security import get_password_hash

def get_usuarios(db: Session, clinica_id: int = None, skip: int = 0, limit: int = 100):
    """Retorna usuários. Se clinica_id for passado, filtra os usuários daquela clínica."""
    query = db.query(Usuario)
    if clinica_id:
        query = query.filter(Usuario.clinica_id == clinica_id)
    return query.offset(skip).limit(limit).all()

def create_usuario(db: Session, user: UsuarioCreate):
    """Cria um novo usuário colaborador ou master no banco MASTER."""
    existente = db.query(Usuario).filter(Usuario.email == user.email).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado no sistema."
        )
    
    hashed_password = get_password_hash(user.senha)
    
    novo_usuario = Usuario(
        nome=user.nome,
        email=user.email,
        senha_hash=hashed_password,
        tipo_usuario=user.tipo_usuario,
        clinica_id=user.clinica_id
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario
