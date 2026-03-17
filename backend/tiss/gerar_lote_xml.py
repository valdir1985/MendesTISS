from sqlalchemy.orm import Session
from datetime import datetime
import hashlib

from backend.models.lote import LoteTiss, LoteGuia
from backend.models.guia import Guia, GuiaProcedimento
from backend.models.convenio import Convenio
from backend.models.paciente import Paciente
from backend.models.medico import Medico
from backend.models.procedimento import Procedimento

def gerar_xml_tiss_lote(db: Session, lote_id: int) -> str:
    # 1. Buscar o Lote e o Convénio
    lote = db.query(LoteTiss).filter(LoteTiss.id == lote_id).first()
    if not lote:
        raise ValueError("Lote não encontrado.")

    convenio = db.query(Convenio).filter(Convenio.id == lote.convenio_id).first()
    
    # 2. Buscar as guias associadas ao lote
    lote_guias = db.query(LoteGuia).filter(LoteGuia.lote_id == lote.id).all()
    guias_ids = [lg.guia_id for lg in lote_guias]
    guias = db.query(Guia).filter(Guia.id.in_(guias_ids)).all()

    data_hora_atual = datetime.now()
    data_formatada = data_hora_atual.strftime("%Y-%m-%d")
    hora_formatada = data_hora_atual.strftime("%H:%M:%S")

    # 3. Iniciar a construção do XML TISS
    xml = f"""<?xml version="1.0" encoding="ISO-8859-1"?>
<ans:mensagemTISS xmlns:ans="http://www.ans.gov.br/padroes/tiss/schemas" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <ans:cabecalho>
        <ans:identificacaoTransacao>
            <ans:tipoTransacao>ENVIO_LOTE_GUIAS</ans:tipoTransacao>
            <ans:sequencialTransacao>{lote.id}</ans:sequencialTransacao>
            <ans:dataRegistroTransacao>{data_formatada}</ans:dataRegistroTransacao>
            <ans:horaRegistroTransacao>{hora_formatada}</ans:horaRegistroTransacao>
        </ans:identificacaoTransacao>
        <ans:origem>
            <ans:identificacaoPrestador>
                <ans:CNPJ>00000000000000</ans:CNPJ> </ans:identificacaoPrestador>
        </ans:origem>
        <ans:destino>
            <ans:registroANS>{convenio.registro_ans}</ans:registroANS>
        </ans:destino>
        <ans:Padrao>{convenio.versao_tiss}</ans:Padrao>
    </ans:cabecalho>
    <ans:prestadorParaOperadora>
        <ans:loteGuias>
            <ans:numeroLote>{lote.numero_lote}</ans:numeroLote>
            <ans:guiasTISS>
"""

    # 4. Iterar sobre cada guia para adicionar ao XML
    for guia in guias:
        paciente = db.query(Paciente).filter(Paciente.id == guia.paciente_id).first()
        medico = db.query(Medico).filter(Medico.id == guia.medico_executante_id).first()
        itens = db.query(GuiaProcedimento).filter(GuiaProcedimento.guia_id == guia.id).all()
        
        numero_guia = guia.numero_guia_prestador or str(guia.id).zfill(8)

        # Estrutura de exemplo baseada na Guia SP-SADT (suporta múltiplos procedimentos)
        xml += f"""                <ans:guiaSP-SADT>
                    <ans:cabecalhoGuia>
                        <ans:registroANS>{convenio.registro_ans}</ans:registroANS>
                        <ans:numeroGuiaPrestador>{numero_guia}</ans:numeroGuiaPrestador>
                    </ans:cabecalhoGuia>
                    <ans:dadosBeneficiario>
                        <ans:numeroCarteira>{paciente.numero_carteira}</ans:numeroCarteira>
                        <ans:nomeBeneficiario>{paciente.nome}</ans:nomeBeneficiario>
                    </ans:dadosBeneficiario>
                    <ans:dadosSolicitante>
                        <ans:profissionalSolicitante>
                            <ans:nomeProfissional>{medico.nome}</ans:nomeProfissional>
                            <ans:conselhoProfissional>{medico.crm}</ans:conselhoProfissional>
                            <ans:UF>{medico.uf_crm}</ans:UF>
                            <ans:CBOS>{medico.cbo}</ans:CBOS>
                        </ans:profissionalSolicitante>
                    </ans:dadosSolicitante>
                    <ans:procedimentosExecutados>
"""
        # 5. Iterar sobre os procedimentos da guia
        for item in itens:
            procedimento = db.query(Procedimento).filter(Procedimento.id == item.procedimento_id).first()
            xml += f"""                        <ans:procedimentoExecutado>
                            <ans:dataExecucao>{guia.data_atendimento}</ans:dataExecucao>
                            <ans:horaInicial>{hora_formatada}</ans:horaInicial>
                            <ans:horaFinal>{hora_formatada}</ans:horaFinal>
                            <ans:procedimento>
                                <ans:codigoTabela>22</ans:codigoTabela>
                                <ans:codigoProcedimento>{procedimento.codigo}</ans:codigoProcedimento>
                                <ans:descricaoProcedimento>{procedimento.descricao}</ans:descricaoProcedimento>
                            </ans:procedimento>
                            <ans:quantidadeExecutada>{item.quantidade}</ans:quantidadeExecutada>
                            <ans:valorUnitario>{item.valor_unitario}</ans:valorUnitario>
                            <ans:valorTotal>{item.valor_total}</ans:valorTotal>
                        </ans:procedimentoExecutado>
"""
        
        xml += f"""                    </ans:procedimentosExecutados>
                    <ans:valorTotal>
                        <ans:valorProcedimentos>{guia.valor_total}</ans:valorProcedimentos>
                        <ans:valorTotalGeral>{guia.valor_total}</ans:valorTotalGeral>
                    </ans:valorTotal>
                </ans:guiaSP-SADT>
"""

    # Fechar as tags principais
    xml_fechamento = """            </ans:guiasTISS>
        </ans:loteGuias>
    </ans:prestadorParaOperadora>
"""
    xml += xml_fechamento

    # 6. Cálculo do Hash TISS (MD5 de todo o conteúdo exceto a tag epilogo)
    hash_md5 = hashlib.md5(xml.encode('ISO-8859-1')).hexdigest()

    xml += f"""    <ans:epilogo>
        <ans:hash>{hash_md5}</ans:hash>
    </ans:epilogo>
</ans:mensagemTISS>"""

    return xml
