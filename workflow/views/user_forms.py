from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from workflow.forms import RegisterForm

def register(request):
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
    
        if form.is_valid():
            salvar = form.save()
            messages.success(request, 'Ususário Cadastrado com Sucesso!')
            
    return render(
        request,
        'workflow/register.html',
        {
            'form': form
        }
    )