# Generated by Django 5.1 on 2024-08-31 02:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0003_alter_servico_tipo_servico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servico',
            name='prazo_execucao',
        ),
    ]
