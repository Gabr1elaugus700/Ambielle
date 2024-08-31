from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from workflow.forms import CreateCliente, CreateServicoForm
from django.contrib import messages

def createCliente(request):

    if request.method == 'POST':

        title = 'Cadastro De Clientes'
        form = CreateCliente(request.POST)

        context ={
            'title': title,
            'form': form,
        }

        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente Cadastrado com Sucesso!')
            return redirect('workflow:createCliente')

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
    
def createServico(request):
    if request.method == 'POST':

        title = 'Cadastro de Serviços'
        form = CreateServicoForm(request.POST)

        context ={
            'title': title,
            'form': form,
        }

        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço Cadastrado com Sucesso!')
            return redirect('workflow:createServico')

        return render(
            request,
            'workflow/createServico.html',
            context,
        )
    
    else:
        print('tO AQUI')
        title = 'Cadastro de Serviço'
        context = {
            'title': title,
            'form': CreateServicoForm
        }

        return render(
            request, 
            'workflow/createServico.html',
            context,
        )