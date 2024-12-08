from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from workflow.forms import CreateCliente, CreateTarefaForm, CreateServico
from workflow.models import Cliente, TipoServico
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required(login_url='workflow:login')
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

@login_required(login_url='workflow:login')   
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

@login_required(login_url='workflow:login')      
def deleteClientes(request, cliente_id):
    cliente_id = get_object_or_404(Cliente, id=cliente_id)
    cliente_id.delete()
    
    
    messages.warning(request, 'Cliente Deletado!')
    
    return redirect('workflow:getCliente')

@login_required(login_url='workflow:login')   
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

@login_required(login_url='workflow:login')   
def createTipoServico(request):
    if request.method == 'POST':

        title = 'Cadastro de tipos de Serviços'
        form = CreateServico(request.POST)

        context ={
            'title': title,
            'form': form,
        }

        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço Cadastrado com Sucesso!')
            return redirect('workflow:tipoServico')

        return render(
            request,
            'workflow/createServico.html',
            context,
        )
    
    else:
        title = 'Cadastro de tipos de Serviço'
        
        
        tipos_ser = TipoServico.objects.all()
        paginator = Paginator(tipos_ser, 15)
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
        
        context = {
            'title': title,
            'form': CreateServico,
            'page_obj': page_obj
        }

        return render(
            request, 
            'workflow/tipoServico.html',
            context,
        )


def updateTipoServico(request, servico_id=None):
    servico = None
    if servico_id:
        servico = get_object_or_404(TipoServico, pk=servico_id)

    if request.method == 'POST':
        form = CreateServico(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço salvo com sucesso!')
            return redirect('workflow:tipoServico')  # Redirecione para a lista após salvar
    else:
        form = CreateServico(instance=servico)

    form_action = reverse('workflow:updateTipoServico', args=(servico_id,)) if servico else reverse('workflow:tipoServico')

    return render(
        request,
        'workflow/tipoServico.html',
        {
            'form': form,
            'form_action': form_action,
            'servico': servico,
        },
    )

# def deleteTipoServico(request, servico_id):
#     servico = get_object_or_404(TipoServico, pk=servico_id)

#     if request.method == "POST":
#         servico.delete()
#         messages.success(request, 'Serviço excluído com sucesso!')
#         return redirect('workflow:tipoServico')  # Redirecione para a página de listagem
    
#     messages.error(request, 'A exclusão falhou. Tente novamente.')
#     return redirect('workflow:tipoServico')

def deleteTipoServico(request, servico_id):
    servico_id = get_object_or_404(TipoServico, id=servico_id)
    servico_id.delete()
    
    
    messages.warning(request, 'Serviço Excluido!')
    
    return redirect('workflow:tipoServico')