from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
import time

from .models import *
from .utils import cookieCart, cartData, guestOrder

from django.contrib.auth.models import User

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.signals import user_logged_in

from django.db.models import Q

@receiver(user_logged_in)
def add_items_to_cart(sender, user, request, **kwargs):
    cookieData = cookieCart(request)
    items = cookieData["items"]
    customer = user.cliente
    order, created = Carrinho.objects.get_or_create(customer=customer, complete=False)

    for item in items:
        product = Produto.objects.get(id=item["product"]["id"])
        CarrinhoItem.objects.create(
            product=product, order=order, quantity=item["quantity"], size=item["size"]
        )

    request.session['clear_cart_cookie'] = True



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        raw_password = request.POST["password"]
        email = request.POST["email"]

        try:
            validate_email(email)
        except ValidationError:
            pass

        user = User.objects.create_user(
            username=username, email=email, password=raw_password
        )

        cookieData = cookieCart(request)
        items = cookieData["items"]
        customer = user.cliente
        order, created = Carrinho.objects.get_or_create(customer=customer, complete=False)

        for item in items:
            product = Produto.objects.get(id=item["product"]["id"])
            CarrinhoItem.objects.create(
                product=product, order=order, quantity=item["quantity"], size=item["size"]
            )

        response = redirect("login")
        response.delete_cookie('cart')
        return response

    return render(request, "store/register.html")


def store(request):
    carousel_images = CarouselImage.objects.all()
    data = cartData(request)
    cartItems = data["cartItems"]

    if 'product_ids' in request.session and 'last_update' in request.session and time.time() - request.session['last_update'] < 86400:
        product_ids = request.session['product_ids']
        random_products = Produto.objects.filter(id__in=product_ids)
    else:
        random_products = Produto.objects.exclude(valor_original__isnull=True).order_by('?')[:4]
        request.session['product_ids'] = [product.id for product in random_products]
        request.session['last_update'] = time.time()

    context = {'random_products': random_products, 'carousel_images': carousel_images, "cartItems": cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    for item in items:
        if isinstance(item, CarrinhoItem):
            item.check_availability()

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/cart.html", context)



@login_required(login_url='login')
def checkout(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    size = data['size']

    customer = request.user.cliente
    product = Produto.objects.get(id=productId)
    order, created = Carrinho.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = CarrinhoItem.objects.get_or_create(order=order, product=product, size=size)

    if action == 'add':
        tamanho_produto = TamanhoProduto.objects.get(produto=product, tamanho=size)
        if orderItem.quantity < tamanho_produto.quantidade:
            orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.cliente
        order, created = Carrinho.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data["form"]["total"].replace(",", "."))
    if total == order.get_cart_total:
        order.complete = True
        order.transaction_id = transaction_id
    order.save()

    if order.shipping == True:
        EnderecoEnvio.objects.create(
            customer=customer,
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            zipcode=data["shipping"]["zipcode"],
        )

    if order.complete:
        for item in order.carrinhoitem_set.all():
            if TamanhoProduto.objects.get(produto=item.product, tamanho=item.size).quantidade == 0:
                CarrinhoItem.objects.filter(product=item.product, size=item.size).exclude(order__customer=customer).delete()

    return JsonResponse("Payment complete!", safe=False)


def search_results(request):
    data = cartData(request)
    cartItems = data["cartItems"]

    search_query = request.GET.get("search", "")
    products = Produto.objects.filter(name__icontains=search_query)

    context = {"products": products, "cartItems": cartItems}
    return render(request, "store/search_results.html", context)


from django.db.models import Q

def product_detail(request, product_id):
    data = cartData(request)
    cartItems = data["cartItems"]

    product = Produto.objects.get(id=product_id)

    similar_products = Produto.objects.filter(marca=product.marca, genero=product.genero, departamento_bs=product.departamento_bs).exclude(id=product_id)

    if similar_products.count() < 4:
        similar_products = Produto.objects.filter(
            Q(marca=product.marca) | Q(genero=product.genero) | Q(departamento_bs=product.departamento_bs)
        ).exclude(id=product_id)

    if similar_products.count() < 4:
        num_additional_products = 4 - similar_products.count()
        additional_products = Produto.objects.exclude(id=product_id).order_by('?')[:num_additional_products]
        similar_products = list(similar_products) + list(additional_products)

    if request.user.is_authenticated:
        sizes_in_cart = {item.size: item.quantity for item in CarrinhoItem.objects.filter(product=product, order__customer=request.user.cliente)}
    else:
        sizes_in_cart = {}

    sizes_available = [(size.tamanho, size.quantidade > sizes_in_cart.get(size.tamanho, 0)) for size in product.tamanhoproduto_set.all()]

    if request.user.is_authenticated:
        favoritos_ids = request.user.favorito_set.values_list('product__id', flat=True)
    else:
        favoritos_ids = []

    context = {
        "product": product, 
        "cartItems": cartItems, 
        "sizes_available": sizes_available,
        "favoritos_ids": favoritos_ids,
        "similar_products": similar_products,
    }
    return render(request, "store/product_detail.html", context)

def products(request, category=None):
    if category == 'corrida':
        products = Produto.objects.filter(departamento_bs='Corrida').order_by('-id')[:20]
    elif category == 'colecao':
        products = Produto.objects.all()[:20]
    elif category == 'esportes':
        products = Produto.objects.filter(departamento_bs='Esporte').order_by('-id')[:20]
    elif category == 'promocoes':
        products = Produto.objects.exclude(valor_original__isnull=True).order_by('-id')[:20]
    elif category == 'futebol':
        products = Produto.objects.filter(departamento_bs='Futebol').order_by('-id')[:20]
    elif category == 'lancamentos':
        products = Produto.objects.all().order_by('-id')[:20]
    else:
        products = Produto.objects.none()

    data = cartData(request)
    cartItems = data["cartItems"]
    context = {'products': products,"cartItems": cartItems}
    return render(request, 'store/products.html', context)


def update_favoritos(request):
    if not request.user.is_authenticated:
        request.session['product_id'] = request.POST.get('product_id')
        return redirect_to_login(request.path, login_url='/login/')
    product_id = request.session.pop('product_id', None) or request.POST.get('product_id')
    try:
        product = Produto.objects.get(id=product_id)
    except Produto.DoesNotExist:
        return redirect('product_detail', product_id=product_id)
    favorito, created = Favorito.objects.get_or_create(user=request.user, product=product)
    if not created:  
        favorito.delete()
    return redirect('product_detail', product_id=product.id)


@login_required(login_url='login')
def favoritos(request):
    favoritos = Favorito.objects.filter(user=request.user)
    return render(request, 'store/favoritos.html', {'favoritos': favoritos})