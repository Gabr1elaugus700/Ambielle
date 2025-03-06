from django.shortcuts import render, redirect
from workflow.models import *
from datetime import timedelta
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Prefetch
from workflow.forms import CreateTarefaForm, SuporteForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

@login_required(login_url='workflow:login')
def index(request):
    title = 'Home'

    if request.method == 'POST':
        form = SuporteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workflow:index')  # Redireciona para uma lista de suporte após sucesso
    else:
        form = SuporteForm()

    
    limite = datetime.today().date() + timedelta(days=30)  # Licenças vencendo nos próximos 30 dias
    licencas_proximas = Licenca.objects.filter(data_vencimento__lte=limite)
    clientes = Cliente.objects.count()
    form = CreateTarefaForm()
    # tarefas_em_aberto = Tarefa.objects.filter()

    status_choices = Tarefa.STATUS_CHOICES
    hoje = timezone.now().date()
    data_limite = hoje + timedelta(days=450)
    
    demandas_execucao = Tarefa.objects.filter(status='Execucao', prazo_final__lte=data_limite).order_by('prazo_final')
    demandas_aprovacao = Tarefa.objects.filter(status='Aprovação Cliente', prazo_final__lte=data_limite).order_by('prazo_final')
    demandas_coleta = Tarefa.objects.filter(status='Coleta De Informações', prazo_final__lte=data_limite).order_by('prazo_final')
    demandas_iniciado = Tarefa.objects.filter(status='Iniciado', prazo_final__lte=data_limite).order_by('prazo_final')
    demandas_protocolado = Tarefa.objects.filter(status='Protocolado', prazo_final__lte=data_limite).order_by('prazo_final')
    
    tarefas_em_aberto = (
        demandas_aprovacao.count() + 
        demandas_coleta.count() + 
        demandas_execucao.count() + 
        demandas_iniciado.count() +
        demandas_protocolado.count()
    )

    context ={
        'form': form,
        'title': title,
        'demandas_execucao': demandas_execucao,
        'demandas_aprovacao': demandas_aprovacao,
        'demandas_coleta': demandas_coleta,
        'demandas_iniciado': demandas_iniciado,
        'demandas_protocolado': demandas_protocolado,
        'clientes': clientes, 
        'tarefas_em_aberto': tarefas_em_aberto,
        'licencas': licencas_proximas,
        'status_choices': status_choices
    }

    return render(
        request,
        'workflow/home.html',
        context,
    )

def detalhes_tarefa_api(request, tarefaId):
    tarefa = get_object_or_404(Tarefa, id=tarefaId)
    data = {
        'id': tarefa.id,
        'cliente_id': tarefa.cliente.id,
        'cliente_nome': tarefa.cliente.nome,
        'tipo_servico_id': tarefa.tipo_servico.id,
        'tipo_servico_nome': tarefa.tipo_servico.nome,
        'status': tarefa.status,
        'data_inicio': tarefa.data_inicio.strftime('%Y-%m-%d'),
        'prazo_final': tarefa.prazo_final.strftime('%Y-%m-%d') if tarefa.prazo_final else None,
        'observacoes': tarefa.observacoes,
        'valor_total_servico': tarefa.valor_total_servico,
    }
    return JsonResponse(data)

@login_required(login_url='workflow:login')
def getCliente(request):
    title = 'Lista de Clientes'

    # Busca todos os clientes e otimiza a consulta para incluir as tarefas em aberto
    clientes = Cliente.objects.prefetch_related(
        Prefetch(
            'tarefa_set',  # Substitua 'tarefa_set' pelo related_name definido no modelo, se houver.
            queryset=Tarefa.objects.all(),  # Filtra apenas as tarefas em aberto.
            to_attr='tarefas_em_aberto'  # Armazena as tarefas como um atributo no objeto Cliente.
        )
    )

    # Paginação
    paginator = Paginator(clientes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': title,
        'page_obj': page_obj,
    }

    return render(
        request,
        'workflow/getClientes.html',
        context,
    )



@login_required(login_url='workflow:login')
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

@login_required(login_url='workflow:login')
def getTarefas(request):
    title = 'Tarefas'
    status_selecionados = request.GET.getlist('status', [])
    tipo_servico_selecionados = request.GET.getlist('tipo_servico', [])

    data_inicial = parse_date(request.GET.get('data_inicial', ''))
    data_final = parse_date(request.GET.get('data_final', ''))

    # Busca todas as tarefas inicialmente
    tarefas = Tarefa.objects.all()

    # Criar uma query vazia para adicionar filtros
    query = Q()

    # Aplica filtros apenas se o usuário selecionar algo
    if status_selecionados:
        query &= Q(status__in=status_selecionados)
    
    if tipo_servico_selecionados:
        query &= Q(tipo_servico__id__in=tipo_servico_selecionados)
    
    if data_inicial and data_final:
        query &= Q(prazo_final__range=[data_inicial, data_final])
    elif data_inicial:
        query &= Q(prazo_final__gte=data_inicial)
    elif data_final:
        query &= Q(prazo_final__lte=data_final)

    # Se pelo menos um filtro foi aplicado, filtra os resultados
    if request.GET:  # Se houver parâmetros na URL
        tarefas = tarefas.filter(query)

    # Ordena as tarefas
    tarefas = tarefas.order_by('prazo_final')

    tipo_servico_choices = TipoServico.objects.all()
    status_choices = Tarefa.STATUS_CHOICES

    # Definição de cores para os status
    status_colors = {
        'Iniciado': '#32CD32',
        'Coleta De Informações': '#FF8C00',
        'Execucao': '#00BFFF',
        'Aprovação Cliente': '#FFD700',
        'Concluído': '#32CD32',
        'Encerrado': '#B22222',
    }

    for tarefa in tarefas:
        tarefa.status_color = status_colors.get(tarefa.status, '#000000')

    return render(request, 'workflow/getTarefas.html', {
        'title': title,
        'tarefas': tarefas,
        'status_selecionados': status_selecionados,
        'tipo_servico_selecionados': tipo_servico_selecionados,
        'status_choices': status_choices,
        'tipo_servico_choices': tipo_servico_choices,
        'data_inicial': data_inicial,
        'data_final': data_final,
    })

@login_required(login_url='workflow:login')
def get_tarefas_filtradas(request):
    title = 'Tarefas Filtradas'
    
    # Filtros recebidos do formulário
    cliente_selecionado = request.GET.get('cliente', 'todos')  # Valor padrão: "todos"
    status_selecionados = request.GET.getlist('status', [])  
    data_inicial = parse_date(request.GET.get('data_inicial', ''))
    data_final = parse_date(request.GET.get('data_final', ''))

    # Lista de clientes disponíveis
    clientes = Cliente.objects.all()

    # Se não há filtros aplicados, carregue todas as tarefas
    if not request.GET:
        tarefas = Tarefa.objects.all()
    else:
        tarefas = Tarefa.objects.all()  # Agora, começamos com todas as tarefas
        query = Q()

        # Aplica filtro por cliente, se não for "todos"
        if cliente_selecionado and cliente_selecionado != "todos":
            query &= Q(cliente__id=cliente_selecionado)

        # Aplica filtro por status, se não for "Todos"
        if status_selecionados and 'todos' not in status_selecionados:
            query &= Q(status__in=status_selecionados)

        # Aplica filtro por datas
        if data_inicial and data_final:
            query &= Q(prazo_final__range=[data_inicial, data_final])
        elif data_inicial:
            query &= Q(prazo_final__gte=data_inicial)
        elif data_final:
            query &= Q(prazo_final__lte=data_final)

        # Aplica filtros somente se houver pelo menos um
        if query:
            tarefas = tarefas.filter(query)

    # Ordenação das tarefas
    tarefas = tarefas.order_by('prazo_final')

    # Definição de escolhas de status
    status_choices = [
        ('Iniciado', 'Iniciado'),
        ('Coleta De Informações', 'Coleta de Informações'),
        ('Execucao', 'Execução'),
        ('Aprovação Cliente', 'Aprovação Cliente'),
        ('Concluído', 'Concluído'),
        ('Encerrado', 'Encerrado'),
    ]

    status_colors = {
        'Iniciado': '#32CD32',
        'Coleta De Informações': '#FF8C00',
        'Execucao': '#00BFFF',
        'Aprovação Cliente': '#FFD700',
        'Concluído': '#32CD32',
        'Encerrado': '#B22222',
    }

    for tarefa in tarefas:
        tarefa.status_color = status_colors.get(tarefa.status, '#000000')

    # Passa dados para o template
    return render(request, 'workflow/timeLine.html', {
        'title': title,
        'tarefas': tarefas,
        'clientes': clientes,
        'cliente_selecionado': cliente_selecionado,
        'status_choices': status_choices,
        'status_selecionados': status_selecionados,
        'data_inicial': data_inicial,
        'data_final': data_final,
    })
    
@login_required(login_url='workflow:login')
def getRelatorios(request):
    title = 'Relatórios PDF & XLSX'

    context ={
        'title': title,
    }

    return render(
        request,
        'workflow/relatorios.html',
        context,
    )

@login_required(login_url='workflow:login')
def listaTipoServico(request):
    title = 'Lista de Tipos de Serviço'

    # Buscar todos os serviços
    tipos_servico = TipoServico.objects.all()

    # Paginação: 15 itens por página
    paginator = Paginator(tipos_servico, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Criar um formulário vazio para uso no modal
    # form = CreateServico()

    context = {
        'title': title,
        'page_obj': page_obj # Lista paginada dos serviços
        # 'form': form,  # Formulário para o modal
        # 'form_action': reverse('workflow:createTipoServico')  # URL do cadastro
    }

    return render(request, 'workflow/tipoServico.html', context)

def atualizar_valor_total(request):
    for suporte in Suporte.objects.all():
        suporte.save()
    return HttpResponse("Valor total recalculado e salvo para todos os suportes.")