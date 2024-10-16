from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages, auth
from workflow.forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm

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
    
def login_view(request):
    
    title = 'Login'
    form = AuthenticationForm(request)
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, f'Seja Bem-vindo, {user}')
            return redirect('workflow:index')
        
        messages.error(request, 'Login Inválido!')
    
    return render(
        request,
        'workflow/login.html',
        {
            'form': form,
            'title': title
        }
    )
    
def logout_view(request):
    auth.logout(request)
    return redirect('workflow:login')