from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# --- SCHEMAS PARA OS ITENS DA GUIA ---
class GuiaProcedimentoBase(BaseModel):
    procedimento_id: int
    quantidade: int = 1
    valor_unitario: float

class GuiaProcedimentoCreate(GuiaProcedimentoBase):
    pass

class GuiaProcedimentoResponse(GuiaProcedimentoBase):
    id: int
    guia_id: int
    valor_total: float

    class Config:
        from_attributes = True

# --- SCHEMAS PARA A GUIA PRINCIPAL ---
class GuiaBase(BaseModel):
    paciente_id: int
    medico_executante_id: int
    medico_solicitante_id: Optional[int] = None
    convenio_id: int
    plano_id: int
    tipo_guia: str
    numero_guia_operadora: Optional[str] = None
    data_atendimento: date

class GuiaCreate(GuiaBase):
    # Ao criar a guia, recebemos uma lista de procedimentos a serem inseridos juntos
    procedimentos: List[GuiaProcedimentoCreate]

class GuiaStatusUpdate(BaseModel):
    status: str

class GuiaResponse(GuiaBase):
    id: int
    clinica_id: int # <-- NOVO
    numero_guia_prestador: Optional[str]
    data_emissao: date
    status: str
    valor_total: float
    created_at: datetime
    updated_at: Optional[datetime]
    itens_procedimento: List[GuiaProcedimentoResponse] = []

    class Config:
        from_attributes = True
