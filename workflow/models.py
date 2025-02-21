from django.db import models
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime
from decimal import Decimal

# Modelo para Clientes
class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    numero = models.IntegerField(null=True)
    bairro = models.CharField(max_length=255, blank=True, null=True)
    razao_social = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    contato_principal = models.CharField(max_length=255)
    contato_secundario = models.CharField(max_length=255, blank=True, null=True)
    proposta_link = models.URLField(blank=True, null=True)
    cnpj = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nome}"

class TipoServico(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    orgao = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.nome}"

# Modelo para Serviços
class Servico(models.Model):

    tipo_servico = models.ForeignKey(
        TipoServico,
        on_delete=models.CASCADE,
        related_name="servicos"
    )
    
    descricao = models.TextField(blank=True, null=True) 


    def __str__(self):
        return f"{self.tipo_servico}"


# Modelo para Tarefas
class Tarefa(models.Model):
    STATUS_CHOICES = [
        ('Iniciado', 'Iniciado'),
        ('Coleta De Informações', 'Coleta de Informações'),
        ('Execucao', 'Execução'),
        ('Aprovação Cliente', 'Aprovação Cliente'),
        ('Concluído', 'Concluído'),
        ('Encerrado', 'Encerrado'),
    ]

    tipo_servico = models.ForeignKey(TipoServico, on_delete=models.CASCADE, related_name="tarefas")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='iniciado')
    data_inicio = models.DateField(default=timezone.now)
    prazo_final = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)
    valor_total_servico = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Tarefa {self.id} para {self.cliente.nome}"


# Modelo para Etapas das Tarefas
class Etapa(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE)
    nome_etapa = models.CharField(max_length=255)
    data_etapa = models.DateField(null=True, blank=True)
    status_etapa = models.BooleanField(default=False)
    observacoes_etapa = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Etapa {self.nome_etapa} da Tarefa {self.tarefa.id}"


# Modelo para Suporte
class Suporte(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descricao = models.TextField()
    valor_hora = models.DecimalField(max_digits=10, decimal_places=2, default=75.00)
    data_suporte = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField(blank=True, null=True)

    @property
    def tempo_suporte(self):
        """
        Calcula o tempo total de suporte em horas, somente se 'hora_fim' estiver preenchida.
        """
        if self.hora_inicio and self.hora_fim:
            inicio = make_aware(datetime.combine(self.data_suporte, self.hora_inicio))
            fim = make_aware(datetime.combine(self.data_suporte, self.hora_fim))
            delta = fim - inicio
            return delta.total_seconds() / 3600  # Retorna em horas
        return 0  # Se 'hora_fim' não estiver preenchida, retorna 0

    @property
    def valor_total(self):
        """
        Calcula o valor total do suporte baseado no tempo e no valor por hora.
        """
        return Decimal(self.tempo_suporte) * self.valor_hora  # Converte o tempo para Decimal

    def __str__(self):
        return f"Suporte para {self.cliente.nome} em {self.data_suporte}"
    
# Modelo para Relatórios
class Relatorio(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descricao_relatorio = models.TextField()
    data_relatorio = models.DateField(default=timezone.now)
    tipo_relatorio = models.CharField(max_length=50, choices=[('impressao', 'Impressão'), ('excel', 'Excel')])
    filtro = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Relatório {self.id} para {self.cliente.nome}"

class Licenca(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="licencas")
    descricao = models.CharField(max_length=255)
    data_vencimento = models.DateField()
    tipo_licenca = models.CharField(max_length=20, default='OUTRO')
    renovacao_iniciada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.descricao} - {self.data_vencimento}"