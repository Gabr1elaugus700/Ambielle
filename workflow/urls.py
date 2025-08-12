from django.urls import path
from . import views

app_name = 'workflow'

urlpatterns  = [
    #Detail
    path('ambielle/', views.index, name='index'),
    path('ambielle/timeline/', views.getTimeLine, name='timeline'),
    path('ambielle/listaClientes/', views.getCliente, name='getCliente'),
    path('ambielle/tarefas/', views.get_tarefas_filtradas, name='get_tarefas_filtradas'),
    path('ambielle/listaTipoServico/', views.listaTipoServico, name='listaTipoServico'),
    path('tarefa/<int:tarefa_id>/carregar-formulario/', views.carregar_formulario_edicao, name='carregar_formulario_edicao'),
    
    # path('ambielle/tarefas/', views.getTarefas, name='getTarefas'),
    #Create
    path('ambielle/cadastroCliente/', views.createCliente, name='createCliente'),
    path('ambielle/cadastroTipoServico/', views.createTipoServico, name='tipoServico'),
    path('ambielle/cadastroSuporte/', views.definir_suporte, name='suporte'),
    path('ambielle/cadastroServico/', views.createTarefa, name='createTarefa'),
    path('ambielle/createSuporteForm/', views.createSuporteForm, name='createSuporteForm'),
    path('ambielle/editSuporteForm/<int:suporte_id>/', views.editSuporteForm, name='editSuporteForm'),
    path('api/tarefas/<int:tarefaId>/', views.detalhes_tarefa_api, name='detalhes_tarefa_api'),
    path('api/clientes/', views.clientes_api, name='clientes_api'),

    #Update
    path('ambielle/<int:cliente_id>/update/', views.updateCliente, name='updateCliente'),
    path('ambielle/tipoServico/<int:servico_id>/update/', views.updateTipoServico, name='updateTipoServico'),
    path('ambielle/tarefa/<int:tarefaId>/editar/', views.editar_tarefa, name='editar_tarefa'),
    #Delete
    path('ambielle/<int:cliente_id>/delete/', views.deleteClientes, name='deleteCliente'),
    path('ambielle/tarefa/<int:tarefaId>/delete/', views.excluir_tarefa, name='excluir_tarefa'),
    path('ambielle/tipoServico/<int:id>/delete/', views.deleteTipoServico, name='deleteTipoServico'),
    
    #Relatórios
        #CSV
    path('exportar-xlsx/<str:relatorio_tipo>/', views.export_relatorio_xlsx, name='exportar_xlsx'),
        #PDF
    path('exportar-pdf/<str:relatorio_tipo>/', views.export_relatorio_pdf, name='exportar_pdf'),
    
    #User:
    path('user/register/', views.register, name='register'),
    path('user/update/', views.user_update, name='user_update'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout'),
    
    path('atualizar-valor-total/', views.atualizar_valor_total, name='atualizar_valor_total'),
]