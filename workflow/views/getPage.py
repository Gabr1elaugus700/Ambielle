from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from workflow.forms import CreateCliente, CreateTarefaForm
from django.contrib import messages
from workflow.models import *
from datetime import timedelta
from django.utils.dateparse import parse_date
from django.db.models import Q



def index(request):
    title = 'Home'

    hoje = timezone.now().date()
    data_limite = hoje + timedelta(days=20)
    
    demandas_execucao = Tarefa.objects.filter(status='Execucao', prazo_final__lte=data_limite).order_by('prazo_final')
    demandas_aprovacao = Tarefa.objects.filter(status='Aprovação Cliente', prazo_final__lte=data_limite).order_by('prazo_final')
    demandas_coleta = Tarefa.objects.filter(status='Coleta de Informações', prazo_final__lte=data_limite).order_by('prazo_final')
    demandas_iniciado = Tarefa.objects.filter(status='Iniciado', prazo_final__lte=data_limite).order_by('prazo_final')

    context ={
        'title': title,
        'demandas_execucao': demandas_execucao,
        'demandas_aprovacao': demandas_aprovacao,
        'demandas_coleta': demandas_coleta,
        'demandas_iniciado': demandas_iniciado,
    }

    return render(
        request,
        'workflow/home.html',
        context,
    )
    
def getCliente(request):
    title = 'Lista de Clientes'

    clientes = Cliente.objects.all()

    context ={
        'title': title,
        'clientes': clientes,
    }

    return render(
        request,
        'workflow/getClientes.html',
        context,
    )

def getTimeLine(request):
    title = 'Linha Do Tempo'

    context ={
        'title': title,
    }

    return render(
        request,
        'workflow/timeLine.html',
        context,
    )


def getTarefas(request):
    title = 'Tarefas'
    status_selecionados = request.GET.getlist('status', [])
    tipo_servico_selecionados = request.GET.getlist('tipo_servico', [])

    # Filtrar as tarefas de acordo com os filtros selecionados
    tarefas = Tarefa.objects.all()
    query = Q()
    
    if status_selecionados:
        query |= Q(status__in=status_selecionados)
    
    # Se houver tipos de serviço selecionados, adiciona um filtro OR para tipo de serviço
    if tipo_servico_selecionados:
        query |= Q(tipo_servico__in=tipo_servico_selecionados)
    
    # Aplica o filtro à consulta
    tarefas = tarefas.filter(query).order_by('prazo_final')

    # Passar os filtros selecionados de volta para o template
    return render(request, 'workflow/getTarefas.html', {
        'title': title,
        'tarefas': tarefas,
        'status_selecionados': status_selecionados,
        'tipo_servico_selecionados': tipo_servico_selecionados,
        'status_choices': Tarefa.STATUS_CHOICES,
        'tipo_servico_choices': Tarefa.TIPO_SERVICO_CHOICES
    })