from django.urls import path
from workflow import views

app_name = 'workflow'

urlpatterns  = [
    #Create
    path('ambielle/cadastroCliente/', views.createCliente, name='createCliente'),
    #Detail

    #Update

    #Delete
]