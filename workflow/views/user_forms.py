from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages, auth
from workflow.forms import RegisterForm, RegisterUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def register(request):
    title = 'Cadastro De Usuários'
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
            'title': title,
            'form': form
        }
    )
    
    
@login_required(login_url='workflow:login')
def user_update(request):
    title = 'Atualizar Cadastro'
    form = RegisterUpdateForm(instance=request.user)
    
    if request.method != 'POST':
        return render(
            request,
            'workflow/register.html',
            {
                'title': title,
                'form': form
            }
        )
    
    form = RegisterUpdateForm(data=request.POST, instance=request.user)
    
    if form.is_valid():
        form.save()
        messages.success(request, 'Usuário atualizado com sucesso!')
        
        return render(
        request,
        'workflow/register.html',
        {
            'title': title,
            'form': form
        }
    )
        
    return redirect('workflow:update')

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
    
@login_required(login_url='workflow:login')
def logout_view(request):
    auth.logout(request)
    return redirect('workflow:login')