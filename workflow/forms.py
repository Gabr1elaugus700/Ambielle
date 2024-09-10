from django import forms
from django.core.exceptions import ValidationError
from . import models
from django.contrib.auth.models import User
from .models import Cliente, Tarefa, Servico


class CreateCliente(forms.ModelForm):

    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Digite o Nome',
                'class': 'form-control'
            }
        ),
        label='Nome',
        help_text='obs: Nome de Exibição'
    )

    endereco = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Avenida Colombo'
            }
        ),
        label='Endereço',
        # help_text='Nome de Exibição'
    )

    razao_social = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Razão Social'
            }
        ),
        label='Razão Social',
        # help_text='Nome de Exibição'
    )

    telefone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '(44)99999-1234'
            }
        ),
        label='Telefone',
        # help_text='Nome de Exibição'
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'fulano@dominio.com.br'
            }
        ),
        label='Email',
    )

    contato_principal = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Pedro - (44)99112-3456'
            }
        ),
        label='Contato na Empresa:',
        help_text='Um contato necessário'
    )

    contato_secundario = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Maria - (44)99112-3456'
            }
        ),
        label='Contato Secundário',
        help_text='Não necessário'
    )

    class Meta:
        model = models.Cliente
        fields = ('nome', 'endereco', 'razao_social', 'telefone', 'email', 'contato_principal', 'contato_secundario')


class CreateServicoForm(forms.ModelForm):
    
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Cliente'
    )
    
    tipo_servico = forms.ChoiceField(
        choices=Servico.TIPO_SERVICO_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Tipo de Serviço'
    )
    
    valor_base = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite o valor base'
            }
        ),
        label='Valor Base',
        max_digits=10,
        decimal_places=2
    )
    
    prazo_final = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        ),
        label="Data Limite",
        help_text='Prazo em dias'
    )
    
    class Meta:
        model = Servico
        fields = ['cliente', 'tipo_servico', 'valor_base', 'prazo_final']