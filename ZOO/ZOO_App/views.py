from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
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

def render_shop(request):
    product_list = Produto.objects.all()
    context = {'product_list': product_list,
    }
    return render(request, 'ZOO_App/shop_archive.html', context)

def render_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    return render(request, 'ZOO_App/product_info.html', {'produto': produto})

#@login_required(login_url='/ZOOApp')
def addProductToCart(request):
        produto_set = ProdutoCarinhoCompras_pk.objects.all()
        context = {'produto_set': produto_set,
                   }
        if request.method == 'POST':
            try:
                produto_id = request.POST.get("produto_id")
            except KeyError:
                return render(request, 'ZOO_App/product_info.html', context)
            #request.user.id
            if produto_id:
                produto = get_object_or_404(Produto, pk=produto_id)
                utilizador = get_object_or_404(Utilizador, user_id=request.user.id)
                try:
                    pcc_pk = ProdutoCarinhoCompras_pk.objects.get(produto=produto, utilizador=utilizador)
                except ProdutoCarinhoCompras_pk.DoesNotExist:
                    pcc_pk2 = ProdutoCarinhoCompras_pk(produto=produto, utilizador=utilizador)
                    pcc_pk2.save()
                    pcc1 = ProdutoCarinhoCompras(produtocarinhocompras_pk=pcc_pk2, quantidade=1)
                    pcc1.save()
                    return HttpResponseRedirect(reverse('ZOO_App:shop'))
                #pcc_pk = get_object_or_404(ProdutoCarinhoCompras_pk, pk=questao_id)
                pcc = get_object_or_404(ProdutoCarinhoCompras, produtocarinhocompras_pk=pcc_pk)
                pcc.quantidade+=1
                pcc.save()
                return HttpResponseRedirect(reverse('ZOO_App:shop'))
            else:
                print("Produto selecionado não existe")
        else:
            return render(request, 'ZOO_App/product_info.html', context)