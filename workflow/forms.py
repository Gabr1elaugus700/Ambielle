from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

from .models import Cliente, Tarefa, TipoServico, Suporte


class CreateServico(forms.ModelForm):

    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Digite o Nome',
                'class': 'form-control'
            }
        )
    )
    orgao = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Qual o orgão?',
                'class': 'form-control'
            }
        ),
        label='Orgão Responsavel',
    )    
    
    class Meta:
        model = models.TipoServico
        fields = ('nome', 'orgao')
        

class CreateCliente(forms.ModelForm):
    fantasia = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Fantasia',
                'class': 'form-control'
            }
        ),
        label='Nome',
        help_text='obs: Nome de Exibição'
    )

    endereco = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Avenida Colombo'
            }
        ),
        label='Endereço',
        # help_text='Nome de Exibição'
    )
    
    numero = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '991'
            }
        ),
        label='Numero',
        # help_text='Nome de Exibição'
    )
    bairro = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Centro'
            }
        ),
        label='Bairro',
        # help_text='Nome de Exibição'
    )
    
    cnpj = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Informe o CNPJ'
            }
        ),
        label='CNPJ',
        # help_text='Nome de Exibição'
    )
    

    razao_social = forms.CharField(
        required=True,
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
        required=False,
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
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'fulano@dominio.com.br'
            }
        ),
        label='Email',
    )

    contato_principal = forms.CharField(
        required=False,
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
        required=False,
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
        fields = ('fantasia', 'endereco', 'numero', 'bairro', 'cnpj', 'razao_social', 'telefone', 'email', 'contato_principal', 'contato_secundario')


class CreateTarefaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Cliente'
    )
    
    tipo_servico = forms.ModelChoiceField(
        queryset=models.TipoServico.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Tipo de Serviço'
    )
    
    status = forms.ChoiceField(
        choices=Tarefa.STATUS_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Status'
    )
    
    data_inicio = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        ),
        label="Data de Início"
    )
    
    prazo_final = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        ),
        label="Data Término:"
    )
    
    valor_total_servico = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label="Valor do Serviço",
        required=False
    )
    
    observacoes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label="Observações",
        required=False
    )
    
    class Meta:
        model = Tarefa
        fields = ['cliente', 'tipo_servico', 'status', 'data_inicio', 'prazo_final', 'valor_total_servico', 'observacoes' ]
                
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label='Primeiro Nome',
        min_length=3
    )
    
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
        label='Segundo Nome',
        min_length=3
    )
    
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
        label='Email'
    )
    
    class Meta: 
        model = User
        fields = (
            'first_name', 'last_name', 'email', 
            'username', 'password1', 'password2'
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Email Já existente!', code='invalid')
            )
        
        return email
    
class RegisterUpdateForm(forms.ModelForm):
    
    first_name = forms.CharField(
       min_length=2,
       max_length=30,
       required=True,
       help_text='Obrigatório', 
       error_messages={
           'min_length': 'Por favor, Maior que duas letras'
       }
    )
    
    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    
    password2 = forms.CharField(
        label="Confirme a Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    
    email = forms.EmailField(
        required=True
    )    

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        
        password = cleaned_data.get('password1')
        
        if password: 
            user.set_password(password)
            
        if commit:
            user.save()

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não são iguais')
                )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email
        
        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Email Já existente!', code='invalid')
                )
        
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )
        return password1
    
    class Meta: 
        model = User
        fields = (
            'first_name', 'last_name', 'email', 
            'username', 
        )
        
class SuporteForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Cliente',
        required=True
    )
    
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Descrição',
        required=True,
        min_length=10
    )
    
    valor_hora = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Valor por Hora',
        required=True,
        min_value=0.01,
        max_digits=10,
        decimal_places=2
    )
    
    hora_inicio = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        label='Hora de Início',
        required=True
    )
    
    hora_fim = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        label='Hora de Fim',
        required=False
    )

    class Meta:
        model = Suporte
        fields = ['cliente', 'descricao', 'valor_hora', 'hora_inicio', 'hora_fim']

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fim = cleaned_data.get("hora_fim")

        if hora_inicio and hora_fim and hora_fim < hora_inicio:
            raise forms.ValidationError("A hora de fim não pode ser anterior à hora de início.")