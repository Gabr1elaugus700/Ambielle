import django_filters
from .models import Tarefa

class TarefaDateFilter(django_filters.FilterSet):
    date_inicial = django_filters.DateFilter(field_name='prazo_final', lookup_expr='gte', label='Data Inicial')
    date_final   = django_filters.DateFilter(field_name='prazo_final', lookup_expr='te', label='Data Final')
    
    class Meta:
        model = Tarefa
        fields = []