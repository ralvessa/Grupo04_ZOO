from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


# Create your views here.


def render_index(request):
    return render(request, 'ZOO_App/index.html')


def render_animals_list(request):
    return render(request, 'ZOO_App/listagem_animais.html')


def render_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('ZOO_App:index'))
        else:
            return render(request, 'ZOO_App/login.html')
    return render(request, 'ZOO_App/login.html')


def render_register(request):
    if request.method == 'POST':
        if request.POST.get("password") == request.POST.get("password2"):
            if request.POST.get('username').strip() != '' and request.POST.get('email').strip() != '' and request.POST.get('password').strip() != '' and request.POST.get('first_name').strip() != '' and request.POST.get('last_name').strip() != '' and request.POST.get('address').strip() != '' and request.POST.get('TIN').strip() != '':
                user = User.objects.create_user(request.POST.get("username"), request.POST.get("email"), request.POST.get("password"))
                user.first_name = request.POST.get("first_name")
                user.last_name = request.POST.get("last_name")
                user.save()
                utilizador = Utilizador(user=user, data_nascimento=request.POST.get("birth_date"), morada=request.POST.get("address"), numero_contribuinte=request.POST.get("TIN"))
                utilizador.save()
                user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
                login(request, user)
                return HttpResponseRedirect(reverse('ZOO_App:index'))
            else:
                return render(request, 'ZOO_App/registar.html', {'error_message_empty_fields': "Não pode haver campos vazios!"})
        else:
            return render(request, 'ZOO_App/registar.html', {'error_message_password': "Passwords não são iguais!"})
    else:
        return render(request, 'ZOO_App/registar.html')


@login_required(login_url='/votacao')
def render_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('ZOO_App:login'))

def render_about(request):
    return render(request, 'ZOO_App/about.html')


def render_noticias(request):
    lista_noticias_total = Noticia.objects.all()
    lista_noticias_user = UtilizadorNoticia_pk.objects.filter(utilizador=request.user.utilizador)
    lista_tags = {}
    lista_noticias = []
    lista_noticias_recomendadas = []
    for item in lista_noticias_user:
        noticia = item.noticia
        lista_noticias = lista_noticias + [noticia]
        lista_tags_noticia = NoticiaTag_pk.objects.filter(noticia=noticia)
        for item2 in lista_tags_noticia:
            if lista_tags is not None:
                if item2.tag.nome in lista_tags:
                    lista_tags[item2.tag.nome] = lista_tags[item2.tag.nome] + 1
                else:
                    lista_tags[item2.tag.nome] = 1
            else:
                lista_tags[item2.tag.nome] = 1
    for item in NoticiaTag_pk.objects.all():
        if item.noticia not in lista_noticias and item.tag not in lista_tags.keys():
            lista_noticias_recomendadas = lista_noticias_recomendadas + [item.noticia]
    lista_noticias_recomendadas = lista_noticias_recomendadas + list(lista_noticias_total)
    lista_noticias_recomendadas = lista_noticias_recomendadas[0:4]
    lista_noticias_total = list(lista_noticias_total)
    if "searchTerm" in request.POST:
        searchTerm = request.POST["searchTerm"]
        for item in lista_noticias_total.copy():
            if item.descricao.find(searchTerm) == -1 and item.titulo.find(searchTerm) == -1:
                lista_noticias_total.remove(item)
        for item in lista_noticias_recomendadas.copy():
            if item.descricao.find(searchTerm) == -1 and item.titulo.find(searchTerm) == -1:
                lista_noticias_recomendadas.remove(item)
    return render(request, 'ZOO_App/listagem_noticias.html', {'noticias': lista_noticias_total,'recomendadas': lista_noticias_recomendadas[0:4]})


def render_detalhe_noticia(request):
    return