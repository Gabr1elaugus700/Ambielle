from django.shortcuts import get_object_or_404, render
from django.conf import settings

def index(request):
    title = 'Página de teste'

    context ={
        'title': title,
    }

    return render(
        request,
        'workflow/teste.html',
        context,
    )