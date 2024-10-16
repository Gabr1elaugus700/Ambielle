from django.urls import path
from workflow import views

app_name = 'workflow'

urlpatterns  = [
    #Detail
    path('ambielle/', views.index, name='index'),
    path('ambielle/listaClientes/', views.getCliente, name='getCliente'),
    path('ambielle/linhaTempo/', views.getTimeLine, name='getTimeLine'),
    path('ambielle/tarefas/', views.getTarefas, name='getTarefas'),
    #Create
    path('ambielle/cadastroCliente/', views.createCliente, name='createCliente'),
    
    path('ambielle/cadastroServico/', views.createTarefa, name='createTarefa'),

    #Update
    path('ambielle/<int:cliente_id>/update/', views.updateCliente, name='updateCliente'),
    #Delete
    path('ambielle/<int:cliente_id>/delete/', views.deleteClientes, name='deleteCliente'),
    
    #User:
    path('user/register/', views.register, name='register'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout'),
]