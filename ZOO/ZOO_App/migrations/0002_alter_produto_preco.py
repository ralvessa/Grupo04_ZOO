# Generated by Django 4.1.7 on 2023-05-09 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ZOO_App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='preco',
            field=models.FloatField(),
        ),
    ]
