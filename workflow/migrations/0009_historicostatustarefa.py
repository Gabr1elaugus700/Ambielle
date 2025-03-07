# Generated by Django 5.1 on 2025-02-28 19:40

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0008_licenca'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricoStatusTarefa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Iniciado', 'Iniciado'), ('Coleta De Informações', 'Coleta de Informações'), ('Execucao', 'Execução'), ('Aprovação Cliente', 'Aprovação Cliente'), ('Concluído', 'Concluído'), ('Encerrado', 'Encerrado')], max_length=50)),
                ('data_mudanca', models.DateTimeField(default=django.utils.timezone.now)),
                ('tarefa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historico_status', to='workflow.tarefa')),
            ],
            options={
                'ordering': ['-data_mudanca'],
            },
        ),
    ]
