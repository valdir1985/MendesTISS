from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import timedelta

from backend.database import get_master_db
from backend.config import settings
from backend.schemas.usuario import UsuarioCreate, UsuarioResponse, Token, TokenData
from backend.services import auth_service
from backend.core.security import create_access_token
from backend.models.usuario import Usuario

router = APIRouter()

# OAuth2 config
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


# =========================
# 🔐 USUÁRIO ATUAL (TOKEN)
# =========================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_master_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        token_data = TokenData(email=email)

    except JWTError:
        raise credentials_exception

    user = auth_service.get_user_by_email(db, email=token_data.email)

    if user is None:
        raise credentials_exception

    if not user.ativo:
        raise HTTPException(
            status_code=403,
            detail="Usuário inativo"
        )

    return user


# =========================
# 👤 REGISTRO
# =========================
@router.post("/registrar", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(user: UsuarioCreate, db: Session = Depends(get_master_db)):
    return auth_service.create_user(db=db, user=user)


# =========================
# 🔑 LOGIN
# =========================
@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_master_db)
):
    try:
        # 🔍 Autenticar usuário
        user = auth_service.authenticate_user(
            db,
            form_data.username,
            form_data.password
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos"
            )

        if not user.ativo:
            raise HTTPException(
                status_code=403,
                detail="Usuário inativo"
            )

        # ⏳ Tempo de expiração
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        # 🔐 Gerar token (SEMPRE string segura)
        access_token = create_access_token(
            data={
                "sub": str(user.email),
                "tipo": str(user.tipo_usuario),
                "clinica_id": int(user.clinica_id) if user.clinica_id else None
            },
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        # 🔥 IMPORTANTE: evitar erro 500 silencioso
        print("ERRO NO LOGIN:", str(e))

        raise HTTPException(
            status_code=500,
            detail="Erro interno no login"
        )


# =========================
# 👤 USUÁRIO LOGADO
# =========================
@router.get("/me", response_model=UsuarioResponse)
def ler_usuario_logado(current_user: Usuario = Depends(get_current_user)):
    return current_user
