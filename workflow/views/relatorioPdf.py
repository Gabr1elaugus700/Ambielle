from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from workflow.models import Cliente, Tarefa, Suporte

def export_relatorio_pdf(request, relatorio_tipo):
    """
    Exporta relatórios em PDF com base no tipo de relatório selecionado.
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{relatorio_tipo}.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y_position = height - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, y_position, f"Relatório: {relatorio_tipo.replace('_', ' ').title()}")
    y_position -= 30
    pdf.setFont("Helvetica", 12)

    # RELATÓRIO 1: CLIENTES
    if relatorio_tipo == "clientes":
        pdf.drawString(50, y_position, "ID | Nome | CNPJ | Endereço | Cidade | Telefone | Contato")
        y_position -= 20
        clientes = Cliente.objects.all()
        for cliente in clientes:
            pdf.drawString(50, y_position, f"{cliente.id} | {cliente.nome} | {cliente.cnpj} | {cliente.endereco} | {cliente.bairro} | {cliente.telefone} | {cliente.contato_principal}")
            y_position -= 20

    # RELATÓRIO 2: CLIENTES x SERVIÇOS
    elif relatorio_tipo == "clientes_servicos":
        pdf.drawString(50, y_position, "ID | Cliente | CNPJ | Serviço | Status")
        y_position -= 20
        tarefas = Tarefa.objects.all()
        for tarefa in tarefas:
            pdf.drawString(50, y_position, f"{tarefa.id} | {tarefa.cliente.nome} | {tarefa.cliente.cnpj} | {tarefa.tipo_servico.nome} | {tarefa.status}")
            y_position -= 20

    # RELATÓRIO 3: CLIENTES x SERVIÇOS x VALORES
    elif relatorio_tipo == "clientes_servicos_valores":
        pdf.drawString(50, y_position, "ID | Cliente | CNPJ | Serviço | Valor | Status")
        y_position -= 20
        tarefas = Tarefa.objects.all()
        for tarefa in tarefas:
            pdf.drawString(50, y_position, f"{tarefa.id} | {tarefa.cliente.nome} | {tarefa.cliente.cnpj} | {tarefa.tipo_servico.nome} | {tarefa.valor_total_servico or 'N/A'} | {tarefa.status}")
            y_position -= 20

    # RELATÓRIO 4: CLIENTES x SUPORTE
    elif relatorio_tipo == "clientes_suporte":
        pdf.drawString(50, y_position, "ID | Cliente | CNPJ | Suporte | Valor")
        y_position -= 20
        suportes = Suporte.objects.all()
        for suporte in suportes:
            pdf.drawString(50, y_position, f"{suporte.id} | {suporte.cliente.nome} | {suporte.cliente.cnpj} | {suporte.descricao} | {suporte.valor_total}")
            y_position -= 20

    # RELATÓRIO 5: DEMANDAS POR CLIENTE
    elif relatorio_tipo == "demandas_por_cliente":
        pdf.drawString(50, y_position, "ID | Demanda | Prazo Final | Data de Início | Cliente | CNPJ | Valor")
        y_position -= 20
        tarefas = Tarefa.objects.all()
        for tarefa in tarefas:
            pdf.drawString(50, y_position, f"{tarefa.id} | {tarefa.tipo_servico.nome} | {tarefa.prazo_final or 'N/A'} | {tarefa.data_inicio} | {tarefa.cliente.nome} | {tarefa.cliente.cnpj} | {tarefa.valor_total_servico or 'N/A'}")
            y_position -= 20

    pdf.showPage()
    pdf.save()
    return response
