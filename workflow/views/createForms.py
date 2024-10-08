from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from workflow.forms import CreateCliente, CreateTarefaForm
from workflow.models import Cliente
from django.contrib import messages
from django.urls import reverse

def createCliente(request):
    form_action = reverse('workflow:createCliente')
    
    if request.method == 'POST':
        title = 'Cadastro De Clientes'
        form = CreateCliente(request.POST)

        context ={
            'title': title,
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            cliente = form.save()
            messages.success(request, 'Cliente Cadastrado com Sucesso!')
            return redirect('workflow:updateCliente', cliente_id=cliente.pk)

        return render(
            request,
            'workflow/createClientes.html',
            context,
        )
    
    else:
        title = 'Cadastro De Clientes'
        context = {
            'title': title,
            'form': CreateCliente
        }

        return render(
            request, 
            'workflow/createClientes.html',
            context,
        )
   
def updateCliente(request, cliente_id):
    cliente = get_object_or_404(
        Cliente, pk=cliente_id
    )
    form_action = reverse('workflow:updateCliente', args=(cliente_id,))
    
    if request.method == 'POST':
        title = 'Cadastro De Clientes'
        form = CreateCliente(request.POST, instance=cliente)

        context ={
            'title': title,
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            cliente = form.save()
            messages.success(request, 'Cliente Cadastrado com Sucesso!')
            return redirect('workflow:updateCliente', cliente_id=cliente.pk)

        return render(
            request,
            'workflow/createClientes.html',
            context,
        )
    
    else:
        title = 'Cadastro De Clientes'
        context = {
            'title': title,
            'form': CreateCliente(instance=cliente)
        }

        return render(
            request, 
            'workflow/createClientes.html',
            context,
        )
      
def createTarefa(request):
    if request.method == 'POST':

        title = 'Cadastro de Serviços'
        form = CreateTarefaForm(request.POST)

        context ={
            'title': title,
            'form': form,
        }

        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço Cadastrado com Sucesso!')
            return redirect('workflow:createTarefa')

        return render(
            request,
            'workflow/createServico.html',
            context,
        )
    
    else:
        title = 'Cadastro de Serviço'
        context = {
            'title': title,
            'form': CreateTarefaForm
        }

        return render(
            request, 
            'workflow/createServico.html',
            context,
        )