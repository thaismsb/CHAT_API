# Generated by Django 5.0.6 on 2024-05-26 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='theme',
            new_name='topic',
        ),
    ]
