from django.urls import path
from workflow import views

app_name = 'workflow'

urlpatterns  = [
    #Detail
    path('ambielle/', views.index, name='index'),
    path('ambielle/listaClientes/', views.getCliente, name='getCliente'),
    path('ambielle/linhaTempo/', views.getTimeLine, name='getCliente'),
    #Create
    path('ambielle/cadastroCliente/', views.createCliente, name='createCliente'),
    path('ambielle/cadastroServico/', views.createTarefa, name='createTarefa'),

    #Update

    #Delete
]