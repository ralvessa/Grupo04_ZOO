from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db import transaction
from django.utils import timezone
from django.conf import settings

from .models import *


# Create your views here.


def render_index(request):
    if request.user.is_authenticated:
        list = getProductsInCart(request)
        return render(request, 'ZOO_App/index.html', {'all' :list})
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
    if request.user.is_authenticated:
        list = getProductsInCart(request)
        return render(request, 'ZOO_App/about.html', {'all' :list})
    return render(request, 'ZOO_App/about.html')


def render_noticias(request):
    lista_noticias = Noticia.objects.all()
    if request.user.is_authenticated:
        listcart = getProductsInCart(request)
        lista_noticias_user = []
        lista_tags_user = []
        lista_tags={}
        lista_noticias_recomendadas = []
        listCart = getProductsInCart(request)
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
                      {'noticias': lista_noticias, 'recomendadas': lista_noticias_recomendadas[0:4], 'all' :listcart})
    lista_noticias = list(lista_noticias)
    if "searchTerm" in request.POST:
        searchTerm = request.POST["searchTerm"]
        for item in lista_noticias.copy():
            if item.descricao.find(searchTerm) == -1 and item.titulo.find(searchTerm) == -1:
                lista_noticias.remove(item)
    return render(request, 'ZOO_App/listagem_noticias.html',
                  {'noticias': lista_noticias, 'all' :list})


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
    comments = Comentario.objects.filter(noticia=noticia)
    like_amount = len(UtilizadorNoticia_pk.objects.filter(noticia=noticia, like=True))
    if request.user.is_authenticated:
        try:
            visualizacao = UtilizadorNoticia_pk.objects.get(utilizador=request.user.utilizador, noticia=noticia)
        except UtilizadorNoticia_pk.DoesNotExist:
            visualizacao = UtilizadorNoticia_pk(utilizador=request.user.utilizador, noticia=noticia)
        visualizacao.save()
        list = getProductsInCart(request)
        return render(request, 'ZOO_App/detalhe_noticia.html', {'noticia': noticia, "comments": comments, 'all' :list, "like": visualizacao.like, "like_amount": like_amount})
    return render(request, 'ZOO_App/detalhe_noticia.html', {'noticia': noticia, "comments": comments, "like_amount": like_amount})

def render_precario(request):
    bilhetes = Bilhete.objects.all()
    if request.user.is_authenticated:
        list = getProductsInCart(request)
        return render(request, 'ZOO_App/precario.html', {'bilhete_list' :bilhetes, 'all' :list})
    return render(request, 'ZOO_App/precario.html', {'bilhete_list' :bilhetes})

def render_shop(request):
    product_list = Produto.objects.filter(ativo=True)
    
    product_types=  []
    for product in product_list:
        if product.categoria not in product_types:
            product_types.append(product.categoria)

    if request.user.is_authenticated:
        list = getProductsInCart(request)
        context = {'product_list': product_list,'all' :list, "product_types": product_types
        }
        return render(request, 'ZOO_App/shop_archive.html', context)
    context = {'product_list': product_list, "product_types": product_types
    }
    return render(request, 'ZOO_App/shop_archive.html', context)

def render_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if produto.ativo==False:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/')) 
    if request.user.is_authenticated:
        list = getProductsInCart(request)
        return render(request, 'ZOO_App/product_info.html', {'produto': produto,'all' :list})
    return render(request, 'ZOO_App/product_info.html', {'produto': produto})

#@login_required(login_url='/login')
def addProductToCart(request):
    if request.method == 'POST':
        try:
            produto_id = request.POST.get("produto_id")
            quantidade = request.POST.get("quantidade")
        except KeyError:
            return render(request, 'ZOO_App/shop_archive.html')
        #request.user.id
        if produto_id:
            produto = get_object_or_404(Produto, pk=produto_id)
            if produto.ativo==False:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/')) 
            utilizador = get_object_or_404(Utilizador, user_id=request.user.id)
            try:
                pcc_pk = ProdutoCarinhoCompras_pk.objects.get(produto=produto, utilizador=utilizador)
            except ProdutoCarinhoCompras_pk.DoesNotExist:
                pcc_pk2 = ProdutoCarinhoCompras_pk(produto=produto, utilizador=utilizador, quantidade = quantidade)
                pcc_pk2.save()
                return HttpResponseRedirect(reverse('ZOO_App:shop'))
            #pcc_pk = get_object_or_404(ProdutoCarinhoCompras_pk, pk=questao_id)
            pcc_pk.quantidade+=int('0' + quantidade)
            pcc_pk.save()
            return HttpResponseRedirect(reverse('ZOO_App:shop'))
        else:
            print("Produto selecionado não existe")
    else:
        return render(request, 'ZOO_App/shop_archive.html')  


def auxGetProductsInCart(utilizador):
    pcc_pk = ProdutoCarinhoCompras_pk.objects.filter(utilizador=utilizador)
    list=[]
    for item in pcc_pk:
        if item.produto.ativo==False:
            continue
        list.append(item)
    return list  

def getProductsInCart(request):
    product_list = Produto.objects.all()
    utilizador = get_object_or_404(Utilizador, user_id=request.user.id)
    list = auxGetProductsInCart(utilizador)
    
#    pcc_pk = ProdutoCarinhoCompras_pk.objects.filter(utilizador=utilizador)
#    dict={}
#    for item in pcc_pk:
#        dict[item]=ProdutoCarinhoCompras.objects.get(produtocarinhocompras_pk=item)
        #list.append(ProdutoCarinhoCompras.objects.filter(produtocarinhocompras_pk=item))
    
    #pcc1 = ProdutoCarinhoCompras.objects.filter(produtocarinhocompras_pk=pcc_pk)

    #return render(request, 'ZOO_App/shop_archive.html', {'pcc_pk':pcc_pk, 'pcc': list, 'product_list': product_list})
    #return HttpResponse("{% for key, value in " + dict + ".items %}")
    return list
    #return render(request, 'ZOO_App/shop_archive.html', {'all':dict, 'product_list': product_list})


def render_purchase(request):
    #utilizador = get_object_or_404(Utilizador, user_id=request.user.id)
    #dict = auxGetProductsInCart(utilizador)
    if request.user.is_authenticated:
        list = getProductsInCart(request)
        if len(list)>0:
            return render(request, 'ZOO_App/purchase.html', {'all':list})
        return render_shop(request)


def finishPurchase(request):
    utilizador = get_object_or_404(Utilizador, user_id=request.user.id)
    if request.user.is_authenticated:
        list = auxGetProductsInCart(utilizador)
        current_datetime = timezone.now()  
        precototal = getTotalPrice(list)
        fatura = Fatura(data=current_datetime, preco_total=float(precototal), utilizador=utilizador)
        fatura.save()
        for item in list:
            if item.produto.ativo==False:
                continue
            faturaprodutopk = FaturaProduto_pk(fatura= fatura, produto=item.produto, quantidade=item.quantidade)
            faturaprodutopk.save()
        emptyCart(request)    
        return render_shop(request)

    

def getTotalPrice(list):
    sum = 0
    for item in list:
        sum += item.produto.preco * item.quantidade
    return sum


def emptyCart(request):
    if request.user.is_authenticated:
        product_list = Produto.objects.all()
        utilizador = get_object_or_404(Utilizador, user_id=request.user.id)
        list = auxGetProductsInCart(utilizador) 
        for item in list:
            item.delete()
        return render_shop(request)
    
def deleteProductFromCart(request, produto_id):
    if request.user.is_authenticated:
        utilizador = get_object_or_404(Utilizador, user_id=request.user.id)
        produto = get_object_or_404(Produto, pk=produto_id)
        list = auxGetProductsInCart(utilizador) 
        if produto.ativo==False:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/')) 
        for item in list:
            if item.produto == produto:
                item.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        #return getProductsInCart(request)   
def takeProductFromCart(request, produto_id):
    if request.user.is_authenticated:
        utilizador = get_object_or_404(Utilizador, user_id=request.user.id)
        produto = get_object_or_404(Produto, pk=produto_id)
        list = auxGetProductsInCart(utilizador) 
        if produto.ativo==False:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/')) 
        for item in list:
            if item.produto == produto:
                if item.quantidade > 1:
                    item.quantidade -=1
                    item.save()
                elif item.quantidade==1:
                    return deleteProductFromCart(request, produto_id)               
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def sumProductToCart(request, produto_id):
    if request.user.is_authenticated:
        utilizador = get_object_or_404(Utilizador, user_id=request.user.id)
        produto = get_object_or_404(Produto, pk=produto_id)
        list = auxGetProductsInCart(utilizador) 
        if produto.ativo==False:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/')) 
        for item in list:
            if item.produto == produto:
                item.quantidade +=1
                item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))     
            
def render_minhascompras(request):
    if request.user.is_authenticated:
        list = getProductsInCart(request)
        utilizador = get_object_or_404(Utilizador, user_id=request.user.id)
        faturas = Fatura.objects.filter(utilizador=utilizador)
        bilhetes = BilheteUtilizador.objects.filter(utilizador=request.user.id)
        dict={}
        for item in faturas:
            dict[item]=FaturaProduto_pk.objects.filter(fatura=item)  
        return render(request, 'ZOO_App/minhascompras.html', {'all' :list, 'fatura':dict, 'bilhetes':bilhetes})


def addComentario(request, noticia_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                comentario = request.POST.get("comment")
            except KeyError:
                return render(request, 'ZOO_App/about.html')
        utilizador = get_object_or_404(Utilizador, user_id=request.user.id)
        noticia = get_object_or_404(Noticia, pk=noticia_id)
        current_datetime = timezone.now() 
        #comentario=""
        #list = auxGetProductsInCart(utilizador) 
        utilizador_comentario = Comentario(noticia=noticia, utilizador=utilizador, data=current_datetime, comentario=comentario)
        utilizador_comentario.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))   
    
    
@login_required(login_url='/login')
def render_informacao_pessoal(request):
    list = getProductsInCart(request)
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
        return render(request, 'ZOO_App/informacao_pessoal.html', {'user': user, 'utilizador': utilizador, 'all' :list})
    else:
        return render(request, 'ZOO_App/informacao_pessoal.html', {'user': user, 'utilizador': utilizador, 'all' :list})


@login_required(login_url='/login')
def render_alterar_password(request):
    list = getProductsInCart(request)
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        new_password2 = request.POST['new_password2']
        user = authenticate(username=request.user.username,
                            password=old_password)
        if user is None:
            return render(request, 'ZOO_App/alterar_password.html', {'incorrect_password': 'Password incorreta, tente novamente', 'all' :list})
        else:
            if new_password != new_password2:
                return render(request, 'ZOO_App/alterar_password.html', {'incorrect_password': 'Passwords não são iguais', 'all' :list})
            else:
                user.set_password(new_password)
                user.save()
                login(request, user)
                return render(request, 'ZOO_App/informacao_pessoal.html', {'efective_password_change': 'Alterou a sua password com sucesso', 'all' :list})
    else:
        return render(request, 'ZOO_App/alterar_password.html', {'all' :list})

def bilheteCompra(request,crianca,adulto,senior):
    if(crianca != 0):
        bilheteCrianca = BilheteUtilizador(
            bilhete= Bilhete.objects.get(pk=2), utilizador=User.objects.get(pk=request.user.id),quantidade= crianca)
        bilheteCrianca.save()
    if(adulto != 0):
        bilheteAdulto = BilheteUtilizador(
            bilhete=Bilhete.objects.get(pk=3), utilizador=User.objects.get(pk=request.user.id), quantidade=adulto)
        bilheteAdulto.save()
    if(senior != 0):
        bilheteSenior = BilheteUtilizador(
            bilhete=Bilhete.objects.get(pk=4), utilizador=User.objects.get(pk=request.user.id), quantidade=senior)
        bilheteSenior.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/login')
def render_adicionar_like(request, noticia_id):
    utilizador = Utilizador.objects.get(user=request.user)
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    comments = Comentario.objects.filter(noticia=noticia)
    utilizadornoticia = UtilizadorNoticia_pk.objects.get(utilizador=utilizador, noticia=noticia)
    utilizadornoticia.like = True
    utilizadornoticia.save()
    like_amount = len(UtilizadorNoticia_pk.objects.filter(noticia=noticia, like=True))
    return HttpResponseRedirect(reverse('ZOO_App:detalhe_noticia', args=(noticia_id,)), {'noticia': noticia, "comments": comments, "like": utilizadornoticia.like, "like_amount": like_amount})


@login_required(login_url='/login')
def render_remover_like(request, noticia_id):
    utilizador = Utilizador.objects.get(user=request.user)
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    comments = Comentario.objects.filter(noticia=noticia)
    utilizadornoticia = UtilizadorNoticia_pk.objects.get(utilizador=utilizador, noticia=noticia)
    utilizadornoticia.like = False
    utilizadornoticia.save()
    like_amount = len(UtilizadorNoticia_pk.objects.filter(noticia=noticia, like=True))
    return HttpResponseRedirect(reverse('ZOO_App:detalhe_noticia', args=(noticia_id,)), {'noticia': noticia, "comments": comments, "like": utilizadornoticia.like, "like_amount": like_amount})

def render_createProduct(request):
    if request.user.is_superuser:
        if request.method == "POST" and request.FILES["myfile"]:
            designacao = request.POST['designacao']
            categoria = request.POST['categoria']
            descricao = request.POST['descricao']
            preco = request.POST['preco']
            myfile = request.FILES['myfile']
            produto = Produto(designacao=designacao, categoria=categoria, descricao=descricao, preco=preco, imagem=myfile )
            produto.save()
            return render_shop(request)
        else:
            product_list = Produto.objects.all()  
            product_types=  []
            for product in product_list:
                if product.categoria not in product_types:
                    product_types.append(product.categoria)      
            return render(request, 'ZOO_App/createProduct.html', {"categorias": product_types})

def render_deleteProduct(request, produto_id):
    if request.user.is_superuser:       
        produto = Produto.objects.get(pk=produto_id)
        produto.ativo=False
        produto.save()
        return render_shop(request)
        

def admin_check(user):
    return user.is_superuser


@user_passes_test(admin_check, login_url='/ZOO_App/index')
def render_criar_noticia(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        descricao = request.POST['descricao']
        titulo = request.POST['titulo']
        noticia = Noticia(descricao=descricao, titulo=titulo, imagem=myfile)
        noticia.save()
        return render_detalhe_noticia(request, noticia.id)
    else:
        return render(request, 'ZOO_App/criar_noticia.html')


@user_passes_test(admin_check, login_url='/ZOO_App/index')
def render_remover_noticia(request, noticia_id):
    noticia = Noticia.objects.get(pk=noticia_id)
    noticia.delete()
    return render_noticias(request)