# Generated by Django 4.0.3 on 2022-05-23 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movimento', '0005_arquivo_remove_modelomovimento_data_publicacao'),
    ]

    operations = [
        migrations.RenameField(
            model_name='arquivo',
            old_name='data_publicacao',
            new_name='data_publicacao_banco',
        ),
        migrations.RenameField(
            model_name='arquivo',
            old_name='data_transacao',
            new_name='data_transacao_banco',
        ),
    ]
