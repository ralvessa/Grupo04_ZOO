from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_nascimento = models.DateField()
    morada = models.CharField(max_length=100)
    numero_contribuinte = models.IntegerField()


class Produto(models.Model):
    designacao = models.CharField(max_length=50)
    preco = models.FloatField()
    categoria = models.CharField(max_length=50)
    imagem = models.FileField(upload_to="Products", null=True)
    descricao = models.CharField(max_length=100)


class Fatura(models.Model):
    data = models.DateTimeField()
    preco_total = models.FloatField()
    utilizador = models.ForeignKey(Utilizador, on_delete=models.DO_NOTHING)


class FaturaProduto_pk(models.Model):
    class Meta:
        unique_together = (('fatura', 'produto'),)

    fatura = models.ForeignKey(Fatura, on_delete=models.DO_NOTHING)
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    quantidade = models.IntegerField(default=0)
    


class ProdutoCarinhoCompras_pk(models.Model):
    class Meta:
        unique_together = (('produto', 'utilizador'),)

    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    utilizador = models.ForeignKey(Utilizador, on_delete=models.DO_NOTHING)
    quantidade = models.IntegerField(default = 0)


class Bilhete(models.Model):

    intervalo_idade = models.CharField(max_length=50)
    preco = models.FloatField()


class BilheteUtilizador(models.Model):
    bilhete = models.ForeignKey(Bilhete, on_delete=models.DO_NOTHING)
    utilizador = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data_compra = models.DateTimeField(default=datetime.now)
    quantidade = models.IntegerField()


class Donativo(models.Model):
    utilizador = models.ForeignKey(Utilizador, on_delete=models.DO_NOTHING)
    quantidade = models.FloatField()
    data = models.DateTimeField()


class Tag(models.Model):
    nome = models.CharField(max_length=20)
    descricao = models.CharField(max_length=100)


class Noticia(models.Model):
    imagem = models.FileField(upload_to="noticias", null=True)
    descricao = models.CharField(max_length=200)
    titulo = models.CharField(max_length=20)


class NoticiaTag_pk(models.Model):
    class Meta:
        unique_together = (('noticia', 'tag'),)

    noticia = models.ForeignKey(Noticia, on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)


class UtilizadorNoticia_pk(models.Model):
    class Meta:
        unique_together = (('utilizador', 'noticia'),)

    utilizador = models.ForeignKey(Utilizador, on_delete=models.DO_NOTHING)
    noticia = models.ForeignKey(Noticia, on_delete=models.DO_NOTHING)
    data = models.DateField(default= datetime.now)
    like = models.BooleanField(default=False)

class Comentario(models.Model):
    utilizador = models.ForeignKey(Utilizador, on_delete=models.DO_NOTHING)
    noticia = models.ForeignKey(Noticia, on_delete=models.DO_NOTHING)
    data = models.DateField(default= datetime.now)
    comentario = models.CharField(max_length=200)
    
  

class Especie(models.Model):
    VALORES_CLASSE = [
        ("MAM", "Mamífero"),
        ("REP", "Réptil"),
        ("INS", "Inseto"),
        ("ANF", "Anfíbio"),
        ("ARA", "Aracnídeo"),

    ]
    VALORES_ALIMENTACAO = [
        ("C", "Carnívoro"),
        ("O", "Omnívoro"),
        ("H", "Herbívoro"),
    ]
    VALORES_REGIAO = [
        ("1", "Europa"),
        ("2", "América do Norte"),
        ("3", "América do Sul"),
        ("4", "África"),
        ("5", "Ártico"),
        ("6", "Antártida"),
        ("7", "Austrália"),
        ("8", "Ásia"),
        ("9", "Oceano Pacífico"),
        ("10", "Oceano Atlântico"),
        ("11", "Oceano Ártico"),
        ("12", "Oceano Antártico"),
        ("13", "Oceano Índico"),
    ]
    VALORES_ATIVIDADE = [
        ("N", "Noturno"),
        ("D", "Diurno"),
        ("C", "Crepuscular"),
    ]
    VALORES_VIDA_SOCIAL = [
        ("C", "Casal"),
        ("S", "Solitário"),
        ("B", "Bando"),
    ]
    VALORES_REPRODUCAO = [
        ("O", "Ovípara"),
        ("V", "Vívipara"),
    ]
    nome_especie = models.CharField(max_length=50)
    classe = models.CharField(max_length=3, choices=VALORES_CLASSE)
    alimentacao = models.CharField(max_length=1, choices=VALORES_ALIMENTACAO)
    regiao = models.CharField(max_length=2, choices=VALORES_REGIAO)
    quantidade = models.IntegerField()
    peso = models.CharField(max_length=30)
    comprimento = models.CharField(max_length=30)
    altura = models.CharField(max_length=30)
    atividade = models.CharField(max_length=1, choices=VALORES_ATIVIDADE)
    vida_social = models.CharField(max_length=1, choices=VALORES_VIDA_SOCIAL)
    reproducao = models.CharField(max_length=1, choices=VALORES_REPRODUCAO)
    ameacada = models.IntegerField()
