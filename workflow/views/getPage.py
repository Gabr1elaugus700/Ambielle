from django.shortcuts import get_object_or_404, render
from workflow.models import *
from datetime import timedelta
from django.utils.dateparse import parse_date
from django.db.models import Q
from workflow.filters import TarefaDateFilter

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
    
    # Obtendo as datas da requisição
    data_inicial = parse_date(request.GET.get('data_inicial', ''))
    data_final = parse_date(request.GET.get('data_final', ''))
    
    # Filtrar as tarefas de acordo com os filtros selecionados
    tarefas = Tarefa.objects.all()
    query = Q()
    
    # Filtro por status
    if status_selecionados:
        query &= Q(status__in=status_selecionados)
    
    # Filtro por tipo de serviço
    if tipo_servico_selecionados:
        query &= Q(tipo_servico__in=tipo_servico_selecionados)
    
    # Filtrar pelo prazo_final entre as datas
    if data_inicial and data_final:
        query &= Q(prazo_final__range=[data_inicial, data_final])
    elif data_inicial:
        query &= Q(prazo_final__gte=data_inicial)
    elif data_final:
        query &= Q(prazo_final__lte=data_final)

    # Aplicar o filtro à queryset
    tarefas = tarefas.filter(query).order_by('prazo_final')

    # Renderizar o template com as tarefas filtradas
    return render(request, 'workflow/getTarefas.html', {
        'title': title,
        'tarefas': tarefas,
        'status_selecionados': status_selecionados,
        'tipo_servico_selecionados': tipo_servico_selecionados,
        'status_choices': Tarefa.STATUS_CHOICES,
        'tipo_servico_choices': Tarefa.TIPO_SERVICO_CHOICES,
        'data_inicial': data_inicial,
        'data_final': data_final
    }) 