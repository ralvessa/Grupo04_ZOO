from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db import transaction

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
    lista_noticias = Noticia.objects.all()
    if request.user.is_authenticated:
        lista_noticias_user = []
        lista_tags_user = []
        lista_tags={}
        lista_noticias_recomendadas = []
        for item in UtilizadorNoticia_pk.objects.filter(utilizador=request.user.utilizador):
            lista_noticias_user = lista_noticias_user + [item.noticia]
            for item2 in NoticiaTag_pk.objects.filter(noticia=item.noticia):
                if lista_tags is not None:
                    if item2.tag.nome not in lista_tags:
                        lista_tags[item2.tag.nome] = 1
                else:
                    lista_tags[item2.tag.nome] = 1
        for item in NoticiaTag_pk.objects.all():
            if item.noticia not in lista_noticias and item.tag not in lista_tags.keys():
                lista_noticias_recomendadas = lista_noticias_recomendadas + [item.noticia]
        lista_noticias_recomendadas = lista_noticias_recomendadas + list(lista_noticias)
        lista_noticias_recomendadas = lista_noticias_recomendadas[0:4]
        lista_noticias = list(lista_noticias)
        if "searchTerm" in request.POST:
            searchTerm = request.POST["searchTerm"]
            for item in lista_noticias.copy():
                if item.descricao.find(searchTerm) == -1 and item.titulo.find(searchTerm) == -1:
                    lista_noticias.remove(item)
            for item in lista_noticias_recomendadas.copy():
                if item.descricao.find(searchTerm) == -1 and item.titulo.find(searchTerm) == -1:
                    lista_noticias_recomendadas.remove(item)
        return render(request, 'ZOO_App/listagem_noticias.html',
                      {'noticias': lista_noticias, 'recomendadas': lista_noticias_recomendadas[0:4]})
    lista_noticias = list(lista_noticias)
    if "searchTerm" in request.POST:
        searchTerm = request.POST["searchTerm"]
        for item in lista_noticias.copy():
            if item.descricao.find(searchTerm) == -1 and item.titulo.find(searchTerm) == -1:
                lista_noticias.remove(item)
    return render(request, 'ZOO_App/listagem_noticias.html',
                  {'noticias': lista_noticias,})


    # lista_noticias_total = Noticia.objects.all()
    # lista_noticias_user = UtilizadorNoticia_pk.objects.filter(utilizador=request.user.utilizador)
    # lista_tags = {}
    # lista_noticias = []
    # lista_noticias_recomendadas = []
    # for item in lista_noticias_user:
    #     noticia = item.noticia
    #     lista_noticias = lista_noticias + [noticia]
    #     lista_tags_noticia = NoticiaTag_pk.objects.filter(noticia=noticia)
    #     for item2 in lista_tags_noticia:
    #         if lista_tags is not None:
    #             if item2.tag.nome in lista_tags:
    #                 lista_tags[item2.tag.nome] = lista_tags[item2.tag.nome] + 1
    #             else:
    #                 lista_tags[item2.tag.nome] = 1
    #         else:
    #             lista_tags[item2.tag.nome] = 1
    # for item in NoticiaTag_pk.objects.all():
    #     if item.noticia not in lista_noticias and item.tag not in lista_tags.keys():
    #         lista_noticias_recomendadas = lista_noticias_recomendadas + [item.noticia]
    # lista_noticias_recomendadas = lista_noticias_recomendadas + list(lista_noticias_total)
    # lista_noticias_recomendadas = lista_noticias_recomendadas[0:4]





def render_detalhe_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    if request.user.is_authenticated:
        visualizacao = UtilizadorNoticia_pk(utilizador=request.user.utilizador, noticia=noticia)
        visualizacao.save()
        return render(request, 'ZOO_App/detalhe_noticia.html', {'noticia': noticia})
    return render(request, 'ZOO_App/detalhe_noticia.html', {'noticia': noticia})

def render_precario(request):
    bilhetes = Bilhete.objects.all()
    return render(request, 'ZOO_App/precario.html')

def render_shop(request):
    product_list = Produto.objects.all()
    context = {'product_list': product_list,
    }
    return render(request, 'ZOO_App/shop_archive.html', context)

def render_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    return render(request, 'ZOO_App/product_info.html', {'produto': produto})

#@login_required(login_url='/login')
def addProductToCart(request):
    if request.method == 'POST':
        try:
            produto_id = request.POST.get("produto_id")
            quantidade = request.POST.get("quantidade")
        except KeyError:
            return render(request, 'ZOO_App/shop.html')
        #request.user.id
        if produto_id:
            produto = get_object_or_404(Produto, pk=produto_id)
            utilizador = get_object_or_404(Utilizador, user_id=request.user.id)
            try:
                pcc_pk = ProdutoCarinhoCompras_pk.objects.get(produto=produto, utilizador=utilizador)
            except ProdutoCarinhoCompras_pk.DoesNotExist:
                pcc_pk2 = ProdutoCarinhoCompras_pk(produto=produto, utilizador=utilizador)
                pcc_pk2.save()
                pcc1 = ProdutoCarinhoCompras(produtocarinhocompras_pk=pcc_pk2, quantidade=quantidade)
                pcc1.save()
                return HttpResponseRedirect(reverse('ZOO_App:shop'))
            #pcc_pk = get_object_or_404(ProdutoCarinhoCompras_pk, pk=questao_id)
            pcc = get_object_or_404(ProdutoCarinhoCompras, produtocarinhocompras_pk=pcc_pk)
            pcc.quantidade+=int('0' + quantidade)
            pcc.save()
            return HttpResponseRedirect(reverse('ZOO_App:shop'))
        else:
            print("Produto selecionado não existe")
    else:
        return render(request, 'ZOO_App/shop.html')  

def getProductsInCart(request):
    product_list = Produto.objects.all()

    utilizador = get_object_or_404(Utilizador, user_id=request.user.id)
    pcc_pk = ProdutoCarinhoCompras_pk.objects.filter(utilizador=utilizador)
    #list=[]
    dict={}
    for item in pcc_pk:
        dict[item]=ProdutoCarinhoCompras.objects.get(produtocarinhocompras_pk=item)
        #list.append(ProdutoCarinhoCompras.objects.filter(produtocarinhocompras_pk=item))
    
    #pcc1 = ProdutoCarinhoCompras.objects.filter(produtocarinhocompras_pk=pcc_pk)

    #return render(request, 'ZOO_App/shop_archive.html', {'pcc_pk':pcc_pk, 'pcc': list, 'product_list': product_list})
    return render(request, 'ZOO_App/shop_archive.html', {'all':dict, 'product_list': product_list})

@login_required(login_url='/login')
def render_informacao_pessoal(request):
    user = User.objects.get(id=request.user.id)
    utilizador = Utilizador.objects.get(id=request.user.utilizador.id)
    if request.method == 'POST':
        address = request.POST['address']
        email = request.POST['email']
        if request.user.email != email:
            user.email = email
            user.save()
        if request.user.utilizador.morada != address:
            utilizador.morada = address
            utilizador.save()
        return render(request, 'ZOO_App/informacao_pessoal.html', {'user': user, 'utilizador': utilizador})
    else:
        return render(request, 'ZOO_App/informacao_pessoal.html', {'user': user, 'utilizador': utilizador})


@login_required(login_url='/login')
def render_alterar_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        new_password2 = request.POST['new_password2']
        user = authenticate(username=request.user.username, password=old_password)
        if user is None:
            return render(request, 'ZOO_App/alterar_password.html', {'incorrect_password': 'Password incorreta, tente novamente'})
        else:
            if new_password != new_password2:
                return render(request, 'ZOO_App/alterar_password.html', {'incorrect_password': 'Passwords não são iguais'})
            else:
                user.set_password(new_password)
                user.save()
                login(request, user)
                return render(request, 'ZOO_App/informacao_pessoal.html', {'efective_password_change': 'Alterou a sua password com sucesso'})
    else:
        return render(request, 'ZOO_App/alterar_password.html')

