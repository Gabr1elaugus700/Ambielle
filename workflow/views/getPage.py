from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from workflow.forms import CreateCliente, CreateTarefaForm
from django.contrib import messages
from workflow.models import *
from datetime import timedelta


def index(request):
    title = 'Home'

    hoje = timezone.now().date()
    data_limite = hoje + timedelta(days=20)
    alerta_tarefas = Tarefa.objects.filter(prazo_final__lte=data_limite).order_by('prazo_final')

    context ={
        'title': title,
        'alerta_tarefas': alerta_tarefas,
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
