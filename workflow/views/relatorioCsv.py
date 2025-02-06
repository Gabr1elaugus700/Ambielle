import csv
from django.http import HttpResponse
from workflow.models import Cliente, Tarefa, Suporte

def export_relatorio_csv(request, relatorio_tipo):
    """
    Exporta relatórios em CSV com base no tipo de relatório selecionado.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{relatorio_tipo}.csv"'
    
    writer = csv.writer(response)

    # RELATÓRIO 1: CLIENTES
    if relatorio_tipo == "clientes":
        writer.writerow(['ID', 'Data do Cadastro', 'CNPJ', 'Endereço', 'Cidade', 'Telefone', 'Contato'])
        clientes = Cliente.objects.all()
        for cliente in clientes:
            writer.writerow([
                cliente.id, 
                cliente.nome, 
                cliente.cnpj, 
                cliente.endereco, 
                cliente.bairro, 
                cliente.telefone, 
                cliente.contato_principal
            ])
    
    # RELATÓRIO 2: CLIENTES x SERVIÇOS
    elif relatorio_tipo == "clientes_servicos":
        writer.writerow(['ID', 'Cliente', 'CNPJ', 'Serviço', 'Status'])
        tarefas = Tarefa.objects.all()
        for tarefa in tarefas:
            writer.writerow([
                tarefa.id, 
                tarefa.cliente.nome, 
                tarefa.cliente.cnpj, 
                tarefa.tipo_servico.nome, 
                tarefa.status
            ])

    # RELATÓRIO 3: CLIENTES x SERVIÇOS x VALORES
    elif relatorio_tipo == "clientes_servicos_valores":
        writer.writerow(['ID', 'Cliente', 'CNPJ', 'Serviço', 'Valor', 'Status'])
        tarefas = Tarefa.objects.all()
        for tarefa in tarefas:
            writer.writerow([
                tarefa.id, 
                tarefa.cliente.nome, 
                tarefa.cliente.cnpj, 
                tarefa.tipo_servico.nome, 
                tarefa.valor_total_servico or "N/A", 
                tarefa.status
            ])

    # RELATÓRIO 4: CLIENTES x SUPORTE
    elif relatorio_tipo == "clientes_suporte":
        writer.writerow(['ID', 'Cliente', 'CNPJ', 'Suporte', 'Valor'])
        suportes = Suporte.objects.all()
        for suporte in suportes:
            writer.writerow([
                suporte.id, 
                suporte.cliente.nome, 
                suporte.cliente.cnpj, 
                suporte.descricao, 
                suporte.valor_total
            ])
    
    # RELATÓRIO 5: DEMANDAS POR CLIENTE
    elif relatorio_tipo == "demandas_por_cliente":
        writer.writerow(['ID', 'Demanda/Serviço', 'Prazo Final', 'Data de Início', 'Cliente', 'CNPJ', 'Valores'])
        tarefas = Tarefa.objects.all()
        for tarefa in tarefas:
            writer.writerow([
                tarefa.id, 
                tarefa.tipo_servico.nome, 
                tarefa.prazo_final or "N/A", 
                tarefa.data_inicio, 
                tarefa.cliente.nome, 
                tarefa.cliente.cnpj, 
                tarefa.valor_total_servico or "N/A"
            ])
    
    return response
