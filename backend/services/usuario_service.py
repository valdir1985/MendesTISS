from sqlalchemy.orm import Session
from backend.models.usuario import Usuario
from backend.models.convite import ConviteUsuario
from backend.schemas.usuario import UsuarioUpdate, ConviteCreate
from datetime import datetime, timedelta

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

def get_usuario_by_id(db: Session, user_id: int):
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def update_usuario(db: Session, user_id: int, user_update: UsuarioUpdate):
    db_user = get_usuario_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.commit()
    db.refresh(db_user)
    return db_user

def criar_convite(db: Session, convite: ConviteCreate):
    # O convite expira automaticamente em 7 dias
    expira = datetime.utcnow() + timedelta(days=7)
    novo_convite = ConviteUsuario(
        email=convite.email,
        tipo_usuario=convite.tipo_usuario,
        expira_em=expira
    )
    db.add(novo_convite)
    db.commit()
    db.refresh(novo_convite)
    return novo_convite
