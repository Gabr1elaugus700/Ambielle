# Generated by Django 5.1 on 2024-12-17 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0003_tiposervico_orgao'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarefa',
            name='valor_total_servico',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
