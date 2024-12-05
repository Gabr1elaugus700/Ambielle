from django.contrib import admin
from .models import Cliente, Servico, Tarefa, Etapa, Suporte, Relatorio, TipoServico

# Configuração da exibição dos tipos de serviço no Django Admin
@admin.register(TipoServico)
class TipoServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
    ordering = ('nome',)

# Configuração da exibição dos serviços no Django Admin
@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_servico', 'descricao')
    search_fields = ('tipo_servico__nome', 'descricao')
    list_filter = ('tipo_servico',)
    ordering = ('tipo_servico',)

# Configuração da exibição dos clientes no Django Admin
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'razao_social', 'telefone', 'email', 'contato_principal')
    search_fields = ('nome', 'razao_social', 'email', 'contato_principal')
    list_filter = ('razao_social',)
    ordering = ('nome',)

# Configuração das tarefas no Django Admin
@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'status', 'data_inicio', 'tipo_servico')
    search_fields = ('cliente__nome', 'tipo_servico__nome', 'status')
    list_filter = ('status', 'tipo_servico')
    ordering = ('data_inicio',)
    date_hierarchy = 'data_inicio'


# Configuração das etapas das tarefas
@admin.register(Etapa)
class EtapaAdmin(admin.ModelAdmin):
    list_display = ('tarefa', 'nome_etapa', 'data_etapa', 'status_etapa')
    search_fields = ('tarefa__cliente__nome', 'nome_etapa')
    list_filter = ('status_etapa',)
    ordering = ('data_etapa',)

# Configuração do suporte no Django Admin
@admin.register(Suporte)
class SuporteAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'data_suporte', 'valor_hora', 'hora_inicio', 'hora_fim')
    search_fields = ('cliente__nome',)
    date_hierarchy = 'data_suporte'

# Configuração dos relatórios
@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    list_display = ('tarefa', 'cliente', 'data_relatorio', 'tipo_relatorio')
    search_fields = ('cliente__nome', 'tarefa__tipo_servico__nome', 'tipo_relatorio')
    list_filter = ('tipo_relatorio',)
    date_hierarchy = 'data_relatorio'
