from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models.usuario import Usuario
from backend.schemas.usuario import UsuarioCreate
from backend.core.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def create_user(db: Session, user: UsuarioCreate):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado no sistema."
        )
    
    hashed_password = get_password_hash(user.senha)
    novo_usuario = Usuario(
        nome=user.nome,
        email=user.email,
        senha_hash=hashed_password,
        tipo_usuario=user.tipo_usuario
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

def authenticate_user(db: Session, email: str, senha: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(senha, user.senha_hash):
        return False
    return user
