from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from workflow.forms import CreateCliente, CreateServicoForm
from django.contrib import messages

def index(request):
    title = 'Home'

    context ={
        'title': title,
    }

    return render(
        request,
        'workflow/home.html',
        context,
    )