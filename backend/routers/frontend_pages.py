from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()

# Aponta para a pasta onde estão os arquivos HTML
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/", response_class=HTMLResponse)
def root_redirect():
    """Redireciona a raiz do site direto para o login."""
    return RedirectResponse(url="/login")

@router.get("/login", response_class=HTMLResponse)
def pagina_login(request: Request):
    """Serve a página de login."""
    return templates.TemplateResponse("login.html", {"request": request})

# Apenas um placeholder para o Dashboard para o redirecionamento do login funcionar
@router.get("/dashboard", response_class=HTMLResponse)
def pagina_dashboard(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})
