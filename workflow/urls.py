from django.urls import path
from workflow import views

app_name = 'workflow'

urlpatterns  = [
    #Create
    path('ambielle/teste/', views.index, name='index'),
    #Detail

    #Update

    #Delete
]