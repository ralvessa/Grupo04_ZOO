# Generated by Django 4.1.7 on 2023-05-09 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ZOO_App', '0002_alter_produto_preco'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='imagem',
            field=models.FileField(null=True, upload_to='Products'),
        ),
    ]
