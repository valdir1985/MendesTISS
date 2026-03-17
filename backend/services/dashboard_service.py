from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.models.guia import Guia
from backend.models.lote import LoteTiss
from backend.models.retorno import RetornoGuia, Glosa

def obter_dados_dashboard(db: Session):
    # 1. Resumo Financeiro
    # Soma de todas as guias (Faturado)
    total_faturado = db.query(func.sum(Guia.valor_total)).scalar() or 0.0
    
    # Soma dos valores pagos e glosados (dos retornos da operadora)
    totais_retorno = db.query(
        func.sum(RetornoGuia.valor_pago).label("pago"),
        func.sum(RetornoGuia.valor_glosado).label("glosado")
    ).first()
    
    total_recebido = totais_retorno.pago or 0.0
    total_glosado = totais_retorno.glosado or 0.0
    
    # Valor pendente de recebimento
    valor_a_receber = total_faturado - total_recebido - total_glosado
    if valor_a_receber < 0:
        valor_a_receber = 0.0 # Evita valores negativos por inconsistências
        
    financeiro = {
        "total_faturado": total_faturado,
        "total_recebido": total_recebido,
        "total_glosado": total_glosado,
        "valor_a_receber": valor_a_receber
    }

    # 2. Contagem de Guias por Status (digitada, em_lote, enviada, paga, glosada)
    guias_query = db.query(Guia.status, func.count(Guia.id)).group_by(Guia.status).all()
    status_guias = {status: count for status, count in guias_query}

    # 3. Contagem de Lotes por Status (aberto, enviado)
    lotes_query = db.query(LoteTiss.status, func.count(LoteTiss.id)).group_by(LoteTiss.status).all()
    status_lotes = {status: count for status, count in lotes_query}

    # 4. Status dos Recursos de Glosa
    glosas_query = db.query(Glosa.status_recurso, func.count(Glosa.id)).group_by(Glosa.status_recurso).all()
    glosas_por_recurso = {status: count for status, count in glosas_query}

    return {
        "financeiro": financeiro,
        "status_guias": status_guias,
        "status_lotes": status_lotes,
        "glosas_por_recurso": glosas_por_recurso
    }
