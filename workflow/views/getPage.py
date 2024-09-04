from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from workflow.forms import CreateCliente, CreateServicoForm
from django.contrib import messages
from workflow.models import *


def index(request):
    title = 'Home'

    context ={
        'title': title,
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
