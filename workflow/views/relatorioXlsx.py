import openpyxl
from openpyxl.styles import Font
from django.http import HttpResponse
from workflow.models import Cliente, Tarefa, Suporte

def export_relatorio_xlsx(request, relatorio_tipo):
    """
    Exporta relatórios em Excel (.xlsx) com cabeçalhos em negrito.
    """
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{relatorio_tipo}.xlsx"'

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f'Relatório - {relatorio_tipo.replace("_", " ").title()}'

    # Estilo para os cabeçalhos (Negrito)
    bold_font = Font(bold=True)

    # RELATÓRIO 1: CLIENTES
    if relatorio_tipo == "clientes":
        headers = ['ID', 'Nome do Cliente', 'CNPJ', 'Endereço', 'Cidade', 'Telefone', 'Contato']
        ws.append(headers)

        # Aplica negrito nos cabeçalhos
        for cell in ws[1]:
            cell.font = bold_font

        clientes = Cliente.objects.all()
        for cliente in clientes:
            ws.append([
                cliente.id,
                cliente.nome,
                cliente.cnpj,
                cliente.endereco,
                cliente.bairro if cliente.bairro else "N/A",
                cliente.telefone,
                cliente.contato_principal
            ])
    
    # RELATÓRIO 2: CLIENTES x SERVIÇOS
    elif relatorio_tipo == "clientes_servicos":
        headers = ['ID', 'Cliente', 'CNPJ', 'Serviço', 'Status']
        ws.append(headers)

        for cell in ws[1]:
            cell.font = bold_font

        tarefas = Tarefa.objects.all()
        for tarefa in tarefas:
            ws.append([
                tarefa.id,
                tarefa.cliente.nome,
                tarefa.cliente.cnpj,
                tarefa.tipo_servico.nome,
                tarefa.status
            ])

    # RELATÓRIO 3: CLIENTES x SERVIÇOS x VALORES
    elif relatorio_tipo == "clientes_servicos_valores":
        headers = ['ID', 'Cliente', 'CNPJ', 'Serviço', 'Valor (R$)', 'Status']
        ws.append(headers)

        for cell in ws[1]:
            cell.font = bold_font

        tarefas = Tarefa.objects.all()
        for tarefa in tarefas:
            ws.append([
                tarefa.id,
                tarefa.cliente.nome,
                tarefa.cliente.cnpj,
                tarefa.tipo_servico.nome,
                tarefa.valor_total_servico if tarefa.valor_total_servico else "N/A",
                tarefa.status
            ])

    # RELATÓRIO 4: CLIENTES x SUPORTE
    elif relatorio_tipo == "clientes_suporte":
        headers = ['ID', 'Cliente', 'CNPJ', 'Descrição do Suporte', 'Valor Total (R$)']
        ws.append(headers)

        for cell in ws[1]:
            cell.font = bold_font

        suportes = Suporte.objects.all()
        for suporte in suportes:
            ws.append([
                suporte.id,
                suporte.cliente.nome,
                suporte.cliente.cnpj,
                suporte.descricao,
                suporte.valor_total if suporte.valor_total else "N/A"
            ])
    
    # RELATÓRIO 5: DEMANDAS POR CLIENTE
    elif relatorio_tipo == "demandas_por_cliente":
        headers = ['ID', 'Demanda/Serviço', 'Prazo Final', 'Data de Início', 'Cliente', 'CNPJ', 'Valor (R$)']
        ws.append(headers)

        for cell in ws[1]:
            cell.font = bold_font

        tarefas = Tarefa.objects.all()
        for tarefa in tarefas:
            ws.append([
                tarefa.id,
                tarefa.tipo_servico.nome,
                tarefa.prazo_final.strftime('%d/%m/%Y') if tarefa.prazo_final else "N/A",
                tarefa.data_inicio.strftime('%d/%m/%Y'),
                tarefa.cliente.nome,
                tarefa.cliente.cnpj,
                tarefa.valor_total_servico if tarefa.valor_total_servico else "N/A"
            ])

    wb.save(response)
    return response