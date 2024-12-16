from django.db import models
from django.utils import timezone
from django.utils.timezone import timedelta

# Modelo para Clientes
class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    contato_principal = models.CharField(max_length=255)
    contato_secundario = models.CharField(max_length=255, blank=True, null=True)
    proposta_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome}"

class TipoServico(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    orgao = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.nome}"

# Modelo para Serviços
class Servico(models.Model):
    # # ANVISA = 'Anvisa'
    # # CIVIL = 'Civil'
    # # DEFESA_PF = 'Defesa PF'
    # # EXERCITO = 'Exército'
    # # GESTAO_PROCESSOS = 'Gestão de Processos'
    # # IBAMA = 'Ibama'
    # # ISO_9001 = 'ISO 9001'
    # # IAT = 'IAT'
    # # LIDERANCA = 'Liderança'
    # # MAPA_PF = 'Mapa Da PF'
    # # POLICIA_FEDERAL = 'Polícia Federal'
    # # PRODIR = 'PRODIR'
    # # RDC_ANVISA = 'RDC Anvisa'
    # # RECURSOS_HUMANOS = 'Recursos Humanos'
    # # REGULATORIO = 'Regulatório'
    # # SASSMAQ = 'SASSMAQ'
    # # SINIR = 'SINIR'
    # # TREINAMENTO_EBOOK = 'Treinamento (E-book)'
    # # TREINAMENTO_ONLINE = 'Treinamento (On-line)'
    # # TREINAMENTO_PRESENCIAL = 'Treinamento (Presencial)'

    # TIPO_SERVICO_CHOICES = [
    #     (ANVISA, 'Anvisa'),
    #     (CIVIL, 'Civil'),
    #     (DEFESA_PF, 'Defesa PF'),
    #     (EXERCITO, 'Exército'),
    #     (GESTAO_PROCESSOS, 'Gestão de Processos'),
    #     (IBAMA, 'Ibama'),
    #     (ISO_9001, 'ISO 9001'),
    #     (IAT, 'IAT'),
    #     (LIDERANCA, 'Liderança'),
    #     (MAPA_PF, 'Mapa Da PF'),
    #     (POLICIA_FEDERAL, 'Polícia Federal'),
    #     (PRODIR, 'PRODIR'),
    #     (RDC_ANVISA, 'RDC Anvisa'),
    #     (RECURSOS_HUMANOS, 'Recursos Humanos'),
    #     (REGULATORIO, 'Regulatório'),
    #     (SASSMAQ, 'SASSMAQ'),
    #     (SINIR, 'SINIR'),
    #     (TREINAMENTO_EBOOK, 'Treinamento (E-book)'),
    #     (TREINAMENTO_ONLINE, 'Treinamento (On-line)'),
    #     (TREINAMENTO_PRESENCIAL, 'Treinamento (Presencial)'),
    # ]

   
    tipo_servico = models.ForeignKey(
        TipoServico,
        on_delete=models.CASCADE,  # Define o que acontece se o tipo de serviço for excluído
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
    hora_fim = models.TimeField()

    @property
    def tempo_suporte(self):
        # Calcula a diferença entre hora_fim e hora_inicio
        if self.hora_inicio and self.hora_fim:
            delta = timezone.datetime.combine(self.data_suporte, self.hora_fim) - timezone.datetime.combine(self.data_suporte, self.hora_inicio)
            return delta.total_seconds() / 3600  # Converte para horas
        return 0

    @property
    def valor_total(self):
        return self.tempo_suporte * self.valor_hora

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
