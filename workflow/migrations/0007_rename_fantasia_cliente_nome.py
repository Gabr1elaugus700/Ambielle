# Generated by Django 5.1 on 2025-01-31 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0006_rename_nome_cliente_fantasia_cliente_bairro_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='fantasia',
            new_name='nome',
        ),
    ]
