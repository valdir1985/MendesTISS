import xml.etree.ElementTree as ET
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from datetime import datetime

from backend.models.retorno import RetornoOperadora, RetornoGuia, Glosa
from backend.models.guia import Guia

async def importar_xml_retorno(db: Session, convenio_id: int, file: UploadFile):
    # Lê o conteúdo do arquivo XML enviado
    conteudo = await file.read()
    
    try:
        # Tenta interpretar o XML. O namespace no TISS complica a leitura, então removemos para facilitar a busca
        xml_str = conteudo.decode("ISO-8859-1")
        xml_str = xml_str.replace('ans:', '').replace('xmlns:ans="http://www.ans.gov.br/padroes/tiss/schemas"', '')
        root = ET.fromstring(xml_str)
    except Exception as e:
        raise ValueError(f"Formato XML inválido ou corrompido: {str(e)}")

    # Busca a tag do demonstrativo
    demonstrativo = root.find(".//demonstrativoPagamento")
    if demonstrativo is None:
        raise ValueError("O arquivo não é um Demonstrativo de Pagamento TISS válido.")

    # Extrai o protocolo
    dados_pagamento = demonstrativo.find(".//dadosPagamento")
    protocolo = dados_pagamento.find("numeroProtocolo").text if dados_pagamento is not None and dados_pagamento.find("numeroProtocolo") is not None else "SEM_PROTOCOLO"
    
    # 1. Cria o cabeçalho do Retorno
    db_retorno = RetornoOperadora(
        convenio_id=convenio_id,
        numero_protocolo_retorno=protocolo,
        data_recebimento=datetime.now().date()
    )
    db.add(db_retorno)
    db.flush()

    total_informado = 0.0
    total_pago = 0.0
    total_glosado = 0.0

    # 2. Varre as guias dentro do XML
    relacao_guias = demonstrativo.findall(".//dadosGuia")
    for item_guia in relacao_guias:
        numero_guia_prestador = item_guia.find("numeroGuiaPrestador").text
        
        # Converte os valores financeiros
        val_informado = float(item_guia.find("valorInformadoGuia").text) if item_guia.find("valorInformadoGuia") is not None else 0.0
        val_pago = float(item_guia.find("valorProcessadoGuia").text) if item_guia.find("valorProcessadoGuia") is not None else 0.0
        val_glosado = float(item_guia.find("valorGlosadoGuia").text) if item_guia.find("valorGlosadoGuia") is not None else 0.0

        total_informado += val_informado
        total_pago += val_pago
        total_glosado += val_glosado

        # Busca a guia no nosso banco de dados usando o ID (numero_guia_prestador)
        guia_db = db.query(Guia).filter(Guia.id == int(numero_guia_prestador)).first()
        
        if guia_db:
            # Determina o status da guia baseando-se na glosa
            status_pagamento = "paga"
            if val_glosado > 0 and val_pago > 0:
                status_pagamento = "parcialmente_paga"
            elif val_glosado > 0 and val_pago == 0:
                status_pagamento = "glosada"

            # Atualiza a Guia Principal
            guia_db.status = status_pagamento

            # Cria o registro de Retorno da Guia
            db_retorno_guia = RetornoGuia(
                retorno_id=db_retorno.id,
                guia_id=guia_db.id,
                status_pagamento=status_pagamento,
                valor_informado=val_informado,
                valor_pago=val_pago,
                valor_glosado=val_glosado
            )
            db.add(db_retorno_guia)
            db.flush()

            # 3. Registra as Glosas (se houverem)
            motivos_glosa = item_guia.findall(".//motivosGlosa")
            for glosa in motivos_glosa:
                codigo = glosa.find("codigoGlosa").text if glosa.find("codigoGlosa") is not None else "0000"
                descricao = glosa.find("descricaoGlosa").text if glosa.find("descricaoGlosa") is not None else "Sem descrição"
                valor = float(glosa.find("valorGlosado").text) if glosa.find("valorGlosado") is not None else 0.0
                
                db_glosa = Glosa(
                    retorno_guia_id=db_retorno_guia.id,
                    codigo_glosa=codigo,
                    descricao_glosa=descricao,
                    valor_glosado=valor
                )
                db.add(db_glosa)

    # Atualiza os totais do cabeçalho
    db_retorno.valor_total_informado = total_informado
    db_retorno.valor_total_pago = total_pago
    db_retorno.valor_total_glosado = total_glosado

    db.commit()
    db.refresh(db_retorno)
    
    return db_retorno
