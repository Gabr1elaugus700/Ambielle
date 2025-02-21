from django.contrib import admin
from .models import Cliente, Servico, Tarefa, Etapa, Suporte, Relatorio, TipoServico, Licenca

# Configuração da exibição dos tipos de serviço no Django Admin
@admin.register(TipoServico)
class TipoServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'orgao')
    search_fields = ('nome', 'orgao')
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
    list_display = ('nome', 'razao_social', 'cnpj', 'telefone', 'email', 'contato_principal')
    search_fields = ('nome', 'razao_social', 'cnpj', 'email', 'contato_principal')
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

@admin.register(Licenca)
class LicencaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'cliente', 'data_vencimento', 'tipo_licenca', 'renovacao_iniciada')
    list_filter = ('tipo_licenca', 'renovacao_iniciada', 'data_vencimento')  # Filtros laterais
    search_fields = ('descricao', 'cliente__nome')  # Campo de busca
    ordering = ('data_vencimento',)  # Ordena pela data de vencimento
    list_editable = ('renovacao_iniciada',)  # Permite editar esse campo direto na lista

    # Exibir os detalhes no formulário de edição
    fieldsets = (
        ('Informações da Licença', {
            'fields': ('cliente', 'descricao', 'tipo_licenca')
        }),
        ('Validade', {
            'fields': ('data_vencimento', 'renovacao_iniciada')
        }),
    )