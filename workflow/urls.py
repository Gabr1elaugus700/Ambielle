from django.urls import path
from workflow import views

app_name = 'workflow'

urlpatterns  = [
    #Create
    path('ambielle/cadastroCliente/', views.createCliente, name='createCliente'),
    path('ambielle/cadastroServico/', views.createServico, name='createServico'),
    #Detail

    #Update

    #Delete
]