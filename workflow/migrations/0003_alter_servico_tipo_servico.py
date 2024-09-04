# Generated by Django 5.1 on 2024-08-31 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0002_remove_servico_nome_servico_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='tipo_servico',
            field=models.CharField(choices=[('Anvisa', 'Anvisa'), ('Civil', 'Civil'), ('Defesa PF', 'Defesa PF'), ('Exército', 'Exército'), ('Gestão de Processos', 'Gestão de Processos'), ('Ibama', 'Ibama'), ('ISO 9001', 'ISO 9001'), ('IAT', 'IAT'), ('Liderança', 'Liderança'), ('Mapa Da PF', 'Mapa Da PF'), ('Polícia Federal', 'Polícia Federal'), ('PRODIR', 'PRODIR'), ('RDC Anvisa', 'RDC Anvisa'), ('Recursos Humanos', 'Recursos Humanos'), ('Regulatório', 'Regulatório'), ('SASSMAQ', 'SASSMAQ'), ('SINIR', 'SINIR'), ('Treinamento (E-book)', 'Treinamento (E-book)'), ('Treinamento (On-line)', 'Treinamento (On-line)'), ('Treinamento (Presencial)', 'Treinamento (Presencial)')], max_length=50),
        ),
    ]