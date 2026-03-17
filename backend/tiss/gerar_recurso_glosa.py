from sqlalchemy.orm import Session
from datetime import datetime
import hashlib

from backend.models.recurso_glosa import RecursoGlosa
from backend.models.retorno import Glosa, RetornoGuia, RetornoOperadora
from backend.models.guia import Guia
from backend.models.convenio import Convenio

def gerar_xml_recurso_tiss(db: Session, recurso_id: int) -> str:
    # 1. Buscar as entidades relacionadas
    recurso = db.query(RecursoGlosa).filter(RecursoGlosa.id == recurso_id).first()
    if not recurso:
        raise ValueError("Recurso não encontrado.")
        
    glosa = db.query(Glosa).filter(Glosa.id == recurso.glosa_id).first()
    retorno_guia = db.query(RetornoGuia).filter(RetornoGuia.id == glosa.retorno_guia_id).first()
    retorno_op = db.query(RetornoOperadora).filter(RetornoOperadora.id == retorno_guia.retorno_id).first()
    convenio = db.query(Convenio).filter(Convenio.id == retorno_op.convenio_id).first()
    guia_original = db.query(Guia).filter(Guia.id == retorno_guia.guia_id).first()

    data_hora_atual = datetime.now()
    data_formatada = data_hora_atual.strftime("%Y-%m-%d")
    hora_formatada = data_hora_atual.strftime("%H:%M:%S")

    # 2. Construir o XML (Estrutura Simplificada de Recurso TISS)
    xml = f"""<?xml version="1.0" encoding="ISO-8859-1"?>
<ans:mensagemTISS xmlns:ans="http://www.ans.gov.br/padroes/tiss/schemas" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <ans:cabecalho>
        <ans:identificacaoTransacao>
            <ans:tipoTransacao>ENVIO_RECURSO_GLOSA</ans:tipoTransacao>
            <ans:sequencialTransacao>{recurso.id}</ans:sequencialTransacao>
            <ans:dataRegistroTransacao>{data_formatada}</ans:dataRegistroTransacao>
            <ans:horaRegistroTransacao>{hora_formatada}</ans:horaRegistroTransacao>
        </ans:identificacaoTransacao>
        <ans:origem>
            <ans:identificacaoPrestador>
                <ans:CNPJ>00000000000000</ans:CNPJ>
            </ans:identificacaoPrestador>
        </ans:origem>
        <ans:destino>
            <ans:registroANS>{convenio.registro_ans}</ans:registroANS>
        </ans:destino>
        <ans:Padrao>{convenio.versao_tiss}</ans:Padrao>
    </ans:cabecalho>
    <ans:prestadorParaOperadora>
        <ans:recursoGlosa>
            <ans:dadosRecurso>
                <ans:numeroProtocoloRetorno>{retorno_op.numero_protocolo_retorno}</ans:numeroProtocoloRetorno>
                <ans:numeroGuiaPrestador>{guia_original.numero_guia_prestador or guia_original.id}</ans:numeroGuiaPrestador>
                <ans:recursoGuia>
                    <ans:codigoGlosa>{glosa.codigo_glosa}</ans:codigoGlosa>
                    <ans:justificativaPrestador>{recurso.justificativa}</ans:justificativaPrestador>
                    <ans:valorRecurso>{glosa.valor_glosado}</ans:valorRecurso>
                </ans:recursoGuia>
            </ans:dadosRecurso>
        </ans:recursoGlosa>
    </ans:prestadorParaOperadora>
"""

    # 3. Hash MD5 (Epílogo)
    hash_md5 = hashlib.md5(xml.encode('ISO-8859-1')).hexdigest()

    xml += f"""    <ans:epilogo>
        <ans:hash>{hash_md5}</ans:hash>
    </ans:epilogo>
</ans:mensagemTISS>"""

    return xml
