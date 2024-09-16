from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from workflow.forms import CreateCliente, CreateTarefaForm
from django.contrib import messages
from workflow.models import *
from datetime import timedelta
from django.utils.dateparse import parse_date


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
    title = 'Quadro de Tarefas'
    tarefas = Tarefa.objects.all()

    # Filtrar por status
    status_selecionados = request.GET.getlist('status')
    if status_selecionados:
        tarefas = tarefas.filter(status__in=status_selecionados)

    # Filtrar por tipo de serviço
    tipo_servico_selecionados = request.GET.getlist('tipo_servico')
    if tipo_servico_selecionados:
        tarefas = tarefas.filter(tipo_servico__in=tipo_servico_selecionados)

    context = {
        'tarefas': tarefas,
        'status_choices': Tarefa.STATUS_CHOICES,
        'tipo_servico_choices': Tarefa.TIPO_SERVICO_CHOICES,
        'status_selecionados': status_selecionados,
        'tipo_servico_selecionados': tipo_servico_selecionados,
    }

    return render(request, 'workflow/getTarefas.html', context)