from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import timedelta

# Ajuste nas importações para usar o que está no seu projeto
from backend.database import get_master_db 
from backend.config import settings
from backend.schemas.usuario import UsuarioCreate, UsuarioResponse, Token, TokenData
from backend.services import auth_service
from backend.core.security import create_access_token
from backend.models.usuario import Usuario


from backend.config import settings
from backend.database import engine, Base

from backend.routers import (
auth, clinicas, usuarios, pacientes, medicos, convenios, planos, 
    tabelas, procedimentos, guias, lotes, tiss_engine, retornos, glosas, recursos, dashboard,
    frontend_pages # <-- NOVA IMPORTAÇÃO (Router das páginas HTML)
)

# Importamos os models para garantir a criação das tabelas
from backend.models import (
convite, paciente, medico, convenio, plano, tabela, 
procedimento, guia, lote, retorno, recurso_glosa
)

# Cria as tabelas na base de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
@@ -32,7 +32,15 @@
allow_headers=["*"],
)

# Registo das rotas (Endpoints)
# --- CONFIGURAÇÃO DO FRONTEND ---
# Monta a pasta de arquivos estáticos (CSS, JS) para ser acessível no navegador
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Regista as rotas das páginas HTML (Sem prefixo de API)
app.include_router(frontend_pages.router, tags=["Páginas Web"])


# --- REGISTO DAS ROTAS DA API (Manteve-se igual) ---
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Autenticação"])
app.include_router(clinicas.router, prefix=f"{settings.API_V1_STR}/clinicas", tags=["Clínicas"])
app.include_router(usuarios.router, prefix=f"{settings.API_V1_STR}/usuarios", tags=["Usuários"])
@@ -48,8 +56,4 @@
app.include_router(retornos.router, prefix=f"{settings.API_V1_STR}/retornos", tags=["Retornos"])
app.include_router(glosas.router, prefix=f"{settings.API_V1_STR}/glosas", tags=["Gestão de Glosas"])
app.include_router(recursos.router, prefix=f"{settings.API_V1_STR}/recursos", tags=["Recursos de Glosa"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["Dashboard Financeiro"]) # <-- NOVA ROTA

@app.get("/")
def root():
    return {"message": "Bem-vindo à API Master do sistema de faturamento MendesTiss."}
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["Dashboard Financeiro"])

# O Swagger precisa saber o caminho exato para o campo de login funcionar
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_master_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
        
    # Busca o usuário no banco MASTER
    user = auth_service.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

@router.post("/registrar", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(user: UsuarioCreate, db: Session = Depends(get_master_db)):
    """Cria um novo usuário master ou colaborador."""
    return auth_service.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_master_db)):
    """Autentica o usuário e retorna o JWT."""
    # O email deve ser passado no campo username do formulário
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Incluímos o clinica_id e tipo no token para facilitar o uso no frontend
    access_token = create_access_token(
        data={
            "sub": user.email,
            "tipo": user.tipo_usuario,
            "clinica_id": user.clinica_id
        }, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UsuarioResponse)
def ler_usuario_logado(current_user: Usuario = Depends(get_current_user)):
    return current_user
