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
@router.get("/clinicas", response_class=HTMLResponse)
def pagina_clinicas(request: Request):
    """Serve a página de Gestão de Clínicas."""
    return templates.TemplateResponse("clinicas.html", {"request": request})

@router.get("/pacientes", response_class=HTMLResponse)
def pagina_pacientes(request: Request):
    return templates.TemplateResponse("pacientes.html", {"request": request})

@router.get("/convenios", response_class=HTMLResponse)
def pagina_convenios(request: Request):
    return templates.TemplateResponse("convenios.html", {"request": request})

@router.get("/medicos", response_class=HTMLResponse)
def pagina_medicos(request: Request):
    return templates.TemplateResponse("medicos.html", {"request": request})

@router.get("/guias", response_class=HTMLResponse)
def pagina_guias(request: Request):
    return templates.TemplateResponse("guias.html", {"request": request})

@router.get("/lotes", response_class=HTMLResponse)
def pagina_lotes(request: Request):
    return templates.TemplateResponse("lotes.html", {"request": request})

@router.get("/retornos", response_class=HTMLResponse)
def pagina_retornos(request: Request):
    return templates.TemplateResponse("retornos.html", {"request": request})
