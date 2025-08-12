from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
from workflow.models import Cliente, Tarefa, Suporte

class RelatorioProfissional:
    """
    Classe para gerar relatórios PDF profissionais com design moderno e limpo.
    """
    
    def __init__(self, response, titulo):
        self.response = response
        self.titulo = titulo
        self.doc = SimpleDocTemplate(
            response, 
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=60,
            bottomMargin=60
        )
        self.styles = getSampleStyleSheet()
        self.story = []
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Define estilos customizados para o relatório."""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='TituloPrincipal',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c5aa0')
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='Subtitulo',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#333333')
        ))
        
        # Informações do cabeçalho
        self.styles.add(ParagraphStyle(
            name='InfoCabecalho',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_RIGHT,
            textColor=colors.HexColor('#666666')
        ))
    
    def adicionar_cabecalho(self, filtros_aplicados=None):
        """Adiciona cabeçalho profissional ao relatório."""
        # Título principal
        titulo = Paragraph(self.titulo, self.styles['TituloPrincipal'])
        self.story.append(titulo)
        
        # Informações do relatório
        data_geracao = datetime.now().strftime("%d/%m/%Y às %H:%M")
        info_relatorio = f"<b>Relatório gerado em:</b> {data_geracao}<br/>"
        info_relatorio += f"<b>Sistema:</b> Ambielle - Gestão de Workflow"
        
        if filtros_aplicados:
            info_relatorio += "<br/><b>Filtros aplicados:</b><br/>"
            for filtro, valor in filtros_aplicados.items():
                if valor:
                    info_relatorio += f"• {filtro}: {valor}<br/>"
        
        info_paragraph = Paragraph(info_relatorio, self.styles['InfoCabecalho'])
        self.story.append(info_paragraph)
        self.story.append(Spacer(1, 20))
    
    def adicionar_tabela(self, dados, colunas, titulo_secao=None):
        """Adiciona uma tabela profissional ao relatório com quebra automática de texto."""
        if titulo_secao:
            subtitulo = Paragraph(titulo_secao, self.styles['Subtitulo'])
            self.story.append(subtitulo)
        
        if not dados:
            sem_dados = Paragraph("Nenhum registro encontrado com os filtros aplicados.", self.styles['Normal'])
            self.story.append(sem_dados)
            self.story.append(Spacer(1, 20))
            return
        
        # Configurar larguras específicas por tipo de coluna
        num_colunas = len(colunas)
        largura_pagina = A4[0] - 80  # Margem total
        
        # Definir larguras personalizadas baseadas no conteúdo típico
        if num_colunas == 5:  # Relatórios com 5 colunas
            if 'Descrição' in str(colunas) or 'Demanda' in str(colunas):
                # Para colunas com descrições longas
                col_widths = [
                    largura_pagina * 0.25,  # Nome/Cliente
                    largura_pagina * 0.15,  # CNPJ
                    largura_pagina * 0.35,  # Descrição/Serviço (maior)
                    largura_pagina * 0.12,  # Data/Status
                    largura_pagina * 0.13   # Valor
                ]
            else:
                # Distribuição padrão para 5 colunas
                col_widths = [
                    largura_pagina * 0.25,  # Cliente
                    largura_pagina * 0.15,  # CNPJ
                    largura_pagina * 0.25,  # Serviço
                    largura_pagina * 0.20,  # Status/Data
                    largura_pagina * 0.15   # Valor/Telefone
                ]
        else:
            # Distribuição igual para outros casos
            largura_coluna = largura_pagina / num_colunas
            col_widths = [largura_coluna] * num_colunas
        
        # Preparar dados da tabela com quebra de texto
        tabela_dados = []
        
        # Cabeçalho
        cabecalho = []
        for col in colunas:
            cabecalho.append(Paragraph(f"<b>{col}</b>", self.styles['Normal']))
        tabela_dados.append(cabecalho)
        
        # Dados com quebra automática de texto
        for item in dados:
            linha = []
            for i, valor in enumerate(item):
                if valor is None:
                    valor_str = 'N/A'
                else:
                    valor_str = str(valor)
                
                # Criar Paragraph para quebra automática de texto
                # Ajustar tamanho da fonte baseado no comprimento do texto
                if len(valor_str) > 50:
                    font_size = 7
                elif len(valor_str) > 30:
                    font_size = 8
                else:
                    font_size = 8
                
                # Estilo específico para quebra de texto
                style_quebra = ParagraphStyle(
                    name=f'QuebraTexto_{i}',
                    parent=self.styles['Normal'],
                    fontSize=font_size,
                    leading=font_size + 2,  # Espaçamento entre linhas
                    wordWrap='CJK',  # Quebra otimizada
                    alignment=TA_LEFT,
                    spaceAfter=0,
                    spaceBefore=0
                )
                
                paragraph = Paragraph(valor_str, style_quebra)
                linha.append(paragraph)
            
            tabela_dados.append(linha)
        
        # Criar tabela com altura mínima das linhas
        tabela = Table(
            tabela_dados, 
            colWidths=col_widths, 
            repeatRows=1,
            rowHeights=None  # Altura automática baseada no conteúdo
        )
        
        # Estilo da tabela aprimorado
        tabela.setStyle(TableStyle([
            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            
            # Dados
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),  # Alinhamento superior importante
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('LEFTPADDING', (0, 1), (-1, -1), 6),
            ('RIGHTPADDING', (0, 1), (-1, -1), 6),
            
            # Bordas
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            
            # Linhas alternadas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            
            # Quebra de página e wrapping
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#dddddd')),
            
            # Altura mínima das linhas para acomodar texto quebrado
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ]))
        
        self.story.append(tabela)
        self.story.append(Spacer(1, 20))
    
    def gerar_pdf(self):
        """Gera o PDF final."""
        self.doc.build(self.story)

def export_relatorio_pdf(request, relatorio_tipo):
    """
    Exporta relatórios em PDF com design profissional.
    """
    # Capturar filtros
    data_inicial = request.GET.get("data_inicial")
    data_final = request.GET.get("data_final")
    cliente_nome = request.GET.get("cliente")
    status = request.GET.get("status")
    tipo_servico = request.GET.get("tipo_servico")
    
    # Preparar resposta
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_{relatorio_tipo}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    
    # Mapear títulos dos relatórios
    titulos = {
        'clientes': 'Relatório de Clientes',
        'clientes_servicos': 'Relatório de Clientes x Serviços',
        'clientes_servicos_valores': 'Relatório Financeiro - Clientes x Serviços x Valores',
        'clientes_suporte': 'Relatório de Clientes x Suporte',
        'demandas_por_cliente': 'Relatório de Demandas por Cliente'
    }
    
    titulo = titulos.get(relatorio_tipo, 'Relatório do Sistema')
    relatorio = RelatorioProfissional(response, titulo)
    
    # Preparar filtros para exibição
    filtros_aplicados = {
        'Período': f"{data_inicial or 'Sem filtro'} até {data_final or 'Sem filtro'}" if data_inicial or data_final else None,
        'Cliente': cliente_nome,
        'Status': status,
        'Tipo de Serviço': tipo_servico
    }
    
    def aplicar_filtros(queryset, modelo="tarefa"):
        """Aplica filtros ao queryset baseado nos parâmetros."""
        if cliente_nome:
            if modelo == "cliente":
                queryset = queryset.filter(nome__icontains=cliente_nome)
            else:
                queryset = queryset.filter(cliente__nome__icontains=cliente_nome)
        
        if modelo in ("tarefa", "suporte"):
            data_field = "data_inicio" if modelo == "tarefa" else "data_suporte"
            if data_inicial:
                queryset = queryset.filter(**{f"{data_field}__gte": data_inicial})
            if data_final:
                queryset = queryset.filter(**{f"{data_field}__lte": data_final})
        
        if modelo == "tarefa":
            if status:
                queryset = queryset.filter(status=status)
            if tipo_servico:
                queryset = queryset.filter(tipo_servico__nome__icontains=tipo_servico)
        
        return queryset
    
    # Adicionar cabeçalho
    relatorio.adicionar_cabecalho(filtros_aplicados)
    
    # Gerar relatório específico
    if relatorio_tipo == "clientes":
        clientes = aplicar_filtros(Cliente.objects.all().order_by('nome'), "cliente")
        colunas = ['Nome', 'CNPJ', 'Cidade/UF', 'Telefone', 'Contato Principal']
        dados = [
            [
                cliente.nome,
                cliente.cnpj or 'N/A',
                f"{cliente.bairro}/{cliente.uf}" if cliente.bairro and cliente.uf else 'N/A',
                cliente.telefone or 'N/A',
                cliente.contato_principal or 'N/A'
            ]
            for cliente in clientes
        ]
        relatorio.adicionar_tabela(dados, colunas, f"Total de Clientes: {len(dados)}")
    
    elif relatorio_tipo == "clientes_servicos":
        tarefas = aplicar_filtros(Tarefa.objects.select_related('cliente', 'tipo_servico').order_by('cliente__nome'))
        colunas = ['Cliente', 'CNPJ', 'Serviço', 'Status', 'Data Início']
        dados = [
            [
                tarefa.cliente.nome,
                tarefa.cliente.cnpj or 'N/A',
                tarefa.tipo_servico.nome,
                tarefa.status,
                tarefa.data_inicio.strftime("%d/%m/%Y") if tarefa.data_inicio else 'N/A'
            ]
            for tarefa in tarefas
        ]
        relatorio.adicionar_tabela(dados, colunas, f"Total de Serviços: {len(dados)}")
    
    elif relatorio_tipo == "clientes_servicos_valores":
        tarefas = aplicar_filtros(Tarefa.objects.select_related('cliente', 'tipo_servico').order_by('cliente__nome'))
        colunas = ['Cliente', 'CNPJ', 'Serviço', 'Valor (R$)', 'Status']
        dados = []
        total_geral = 0
        
        for tarefa in tarefas:
            valor = tarefa.valor_total_servico or 0
            total_geral += valor
            dados.append([
                tarefa.cliente.nome,
                tarefa.cliente.cnpj or 'N/A',
                tarefa.tipo_servico.nome,
                f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                tarefa.status
            ])
        
        relatorio.adicionar_tabela(dados, colunas, f"Total de Serviços: {len(dados)} | Valor Total: R$ {total_geral:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    elif relatorio_tipo == "clientes_suporte":
        suportes = aplicar_filtros(Suporte.objects.select_related('cliente').order_by('cliente__nome'), "suporte")
        colunas = ['Cliente', 'CNPJ', 'Descrição do Suporte', 'Data', 'Valor (R$)']
        dados = []
        total_suporte = 0
        
        for suporte in suportes:
            valor = suporte.valor_total or 0
            total_suporte += valor
            
            # Limitar descrição para evitar textos excessivamente longos
            descricao = suporte.descricao
            if len(descricao) > 100:
                descricao = descricao[:97] + "..."
            
            dados.append([
                suporte.cliente.nome,
                suporte.cliente.cnpj or 'N/A',
                descricao,
                suporte.data_suporte.strftime("%d/%m/%Y") if suporte.data_suporte else 'N/A',
                f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            ])
        
        relatorio.adicionar_tabela(dados, colunas, f"Total de Suportes: {len(dados)} | Valor Total: R$ {total_suporte:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    elif relatorio_tipo == "demandas_por_cliente":
        tarefas = aplicar_filtros(Tarefa.objects.select_related('cliente', 'tipo_servico').order_by('cliente__nome', 'prazo_final'))
        colunas = ['Cliente', 'Demanda/Serviço', 'Prazo Final', 'Status', 'Valor (R$)']
        dados = []
        total_demandas = 0
        
        for tarefa in tarefas:
            valor = tarefa.valor_total_servico or 0
            total_demandas += valor
            
            # Tratar textos longos
            cliente_nome = tarefa.cliente.nome
            if len(cliente_nome) > 25:
                cliente_nome = cliente_nome[:22] + "..."
            
            servico_nome = tarefa.tipo_servico.nome
            if len(servico_nome) > 30:
                servico_nome = servico_nome[:27] + "..."
            
            dados.append([
                cliente_nome,
                servico_nome,
                tarefa.prazo_final.strftime("%d/%m/%Y") if tarefa.prazo_final else 'N/A',
                tarefa.status,
                f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            ])
        
        relatorio.adicionar_tabela(dados, colunas, f"Total de Demandas: {len(dados)} | Valor Total: R$ {total_demandas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # Gerar PDF
    relatorio.gerar_pdf()
    return response
