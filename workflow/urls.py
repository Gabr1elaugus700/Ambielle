from django.urls import path
from workflow import views

app_name = 'workflow'

urlpatterns  = [
    #Detail
    path('ambielle/', views.index, name='index'),
    path('ambielle/listaClientes', views.getCliente, name='getCliente'),
    #Create
    path('ambielle/cadastroCliente/', views.createCliente, name='createCliente'),
    path('ambielle/cadastroServico/', views.createServico, name='createServico'),

    #Update

    #Delete
]