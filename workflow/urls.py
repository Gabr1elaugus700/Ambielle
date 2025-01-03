from django.urls import path
from workflow import views

app_name = 'workflow'

urlpatterns  = [
    #Detail
    path('ambielle/', views.index, name='index'),
    path('ambielle/listaClientes/', views.getCliente, name='getCliente'),
    path('ambielle/linhaTempo/', views.get_tarefas_filtradas, name='get_tarefas_filtradas'),
    path('ambielle/tarefas/', views.getTarefas, name='getTarefas'),
    #Create
    path('ambielle/cadastroCliente/', views.createCliente, name='createCliente'),
    path('ambielle/cadastroTipoServico/', views.createTipoServico, name='tipoServico'),
    path('ambielle/cadastroSuporte/', views.definir_suporte, name='suporte'),
    path('ambielle/cadastroServico/', views.createTarefa, name='createTarefa'),

    #Update
    path('ambielle/<int:cliente_id>/update/', views.updateCliente, name='updateCliente'),
    path('ambielle/tipoServico/<int:servico_id>/update/', views.updateTipoServico, name='updateTipoServico'),
    #Delete
    path('ambielle/<int:cliente_id>/delete/', views.deleteClientes, name='deleteCliente'),
    path('ambielle/tipoServico/<int:servico_id>/delete/', views.deleteTipoServico, name='deleteTipoServico'),
    
    #User:
    path('user/register/', views.register, name='register'),
    path('user/update/', views.user_update, name='user_update'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout'),
]