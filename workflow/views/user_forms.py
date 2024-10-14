from django.shortcuts import render
from workflow.forms import RegisterForm

def register(request):
    form = RegisterForm()
    
    return render(
        request,
        'workflow/register.html',
        {
            'form': form
        }
    )