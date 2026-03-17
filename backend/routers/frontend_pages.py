from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()

templates = Jinja2Templates(directory="frontend/templates")

@router.get("/", response_class=HTMLResponse)
def root_redirect():
    return RedirectResponse(url="/login")

@router.get("/login", response_class=HTMLResponse)
def pagina_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
def pagina_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# --- NOVA ROTA ADICIONADA AQUI ---
@router.get("/pacientes", response_class=HTMLResponse)
def pagina_pacientes(request: Request):
    """Serve a página de gestão de Pacientes."""
    return templates.TemplateResponse("pacientes.html", {"request": request})

@router.get("/convenios", response_class=HTMLResponse)
def pagina_convenios(request: Request):
    """Serve a página de gestão de Convênios (Operadoras)."""
    return templates.TemplateResponse("convenios.html", {"request": request})

# --- NOVA ROTA ADICIONADA AQUI ---
@router.get("/medicos", response_class=HTMLResponse)
def pagina_medicos(request: Request):
    """Serve a página de gestão de Médicos."""
    return templates.TemplateResponse("medicos.html", {"request": request})
