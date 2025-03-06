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
        ('Protocolado', 'Protocolado'),  # Nova opção adicionada
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

#Registro das alterações de datas.  
class HistoricoStatusTarefa(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name="historico_status")
    status = models.CharField(max_length=50, choices=Tarefa.STATUS_CHOICES)
    data_mudanca = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Tarefa {self.tarefa.id} mudou para {self.status} em {self.data_mudanca}"

    class Meta:
        ordering = ['-data_mudanca']
        
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
    tempo_suporte = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calcula o tempo_suporte antes de salvar
        if self.hora_inicio and self.hora_fim:
            inicio = datetime.combine(self.data_suporte, self.hora_inicio)
            fim = datetime.combine(self.data_suporte, self.hora_fim)
            delta = fim - inicio
            self.tempo_suporte = Decimal(delta.total_seconds() / 3600)  # Converte para horas
        else:
            self.tempo_suporte = Decimal(0)

        # Calcula o valor_total antes de salvar
        self.valor_total = self.valor_hora * self.tempo_suporte

        super().save(*args, **kwargs)

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