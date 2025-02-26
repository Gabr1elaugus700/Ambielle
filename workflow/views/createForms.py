from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from workflow.forms import CreateCliente, CreateTarefaForm, CreateServico, SuporteForm
from workflow.models import Cliente, TipoServico, Suporte
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from workflow.models import *

@login_required(login_url='workflow:login')
def createCliente(request):
    form = CreateCliente(request.POST or None)
    form_action = reverse('workflow:createCliente')  # ✅ Define o action corretamente

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'success'})

        return JsonResponse({
            'message': 'error',
            'html': render_to_string('workflow/createClientes.html', {'form': form, 'form_action': form_action})
        })

    return render(request, 'workflow/createClientes.html', {'form': form, 'form_action': form_action})

@login_required(login_url='workflow:login')   
def updateCliente(request, cliente_id):
    cliente = get_object_or_404(
        Cliente, pk=cliente_id
    )
    form_action = reverse('workflow:updateCliente', args=(cliente_id,))
    
    if request.method == 'POST':
        form = CreateCliente(request.POST, instance=cliente)

        if form.is_valid():
            cliente = form.save()
            messages.success(request, 'Cliente Cadastrado com Sucesso!')
            return redirect('workflow:updateCliente', cliente_id=cliente.pk)
        
        context ={
            'form': form,
            'form_action': form_action,
        }
        return render(
            request,
            'workflow/createClientes.html',
            context,
        )
    
    else:
        form = CreateCliente(instance=cliente)

        context = {
            'form': form,
            'form_action': form_action,
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
def carregar_formulario_edicao(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    form = CreateTarefaForm(instance=tarefa)  # Preenche o formulário com os dados da tarefa
    return render(request, 'workflow/createServico.html', {'form': form, 'tarefa': tarefa})

@login_required(login_url='workflow:login')
def editar_tarefa(request, tarefa_id):
    if request.method == 'POST':
        tarefa = get_object_or_404(Tarefa, id=tarefa_id)
        form = CreateTarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors})
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)


@login_required(login_url='workflow:login')
def createTipoServico(request):
    form = CreateServico(request.POST or None)
    form_action = reverse('workflow:tipoServico')  # Define o action correto

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço cadastrado com sucesso!')
            return JsonResponse({'message': 'success'})

        return JsonResponse({
            'message': 'error',
            'html': render_to_string('workflow/tipoServicoForm.html', {'form': form, 'form_action': form_action})
        })

    return render(request, 'workflow/tipoServicoForm.html', {'form': form, 'form_action': form_action})

@login_required(login_url='workflow:login')
def updateTipoServico(request, servico_id):
    servico = get_object_or_404(TipoServico, pk=servico_id)
    form_action = reverse('workflow:updateTipoServico', args=[servico_id])

    if request.method == 'POST':
        form = CreateServico(request.POST, instance=servico)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço atualizado com sucesso!')
            return JsonResponse({'message': 'success'})

        return JsonResponse({
            'message': 'error',
            'html': render_to_string('workflow/tipoServicoForm.html', {'form': form, 'form_action': form_action})
        })

    else:
        form = CreateServico(instance=servico)

    return render(
        request,
        'workflow/tipoServicoForm.html',
        {'form': form, 'form_action': form_action}
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


def definir_suporte(request):
    
    title = 'Cadastro de Suporte'
    
    # Obtém o parâmetro 'sort' da URL (caso não exista, usa 'id' como padrão)
    sort_by = request.GET.get('sort', 'id')
    
    # Obtém o parâmetro 'order' da URL (caso não exista, usa 'asc' como padrão)
    order = request.GET.get('order', 'asc')
    
    # Se a ordenação for descendente, adiciona o sinal '-' ao campo de ordenação
    if order == 'desc':
        sort_by = '-' + sort_by
    
    # Obtém os suportes ordenados com base no parâmetro 'sort_by'
    suportes = Suporte.objects.all().order_by(sort_by)
    
    # Paginação - Exibe 10 itens por página
    page_obj = Paginator(suportes, 10).get_page(request.GET.get('page'))
    
    if request.method == 'POST':
        form = SuporteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workflow:suporte')
    else:
        form = SuporteForm()
    
    context = {
        'title': title,
        'form': form,
        'page_obj': page_obj,  # Passa a página de suportes para o template
        'sort_by': sort_by,  # Passa o campo de ordenação para o template
        'order': order,  # Passa o tipo de ordenação (asc/desc) para o template
    }

    return render(request, 'workflow/suporte.html', context)