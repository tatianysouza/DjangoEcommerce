from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cookieCart, cartData, guestOrder

from django.contrib.auth.models import User

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required


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

        return redirect("login")

    return render(request, "store/register.html")


def store(request):
    data = cartData(request)
    cartItems = data["cartItems"]

    products = Produto.objects.all()
    context = {"products": products, "cartItems": cartItems}
    return render(request, "store/store.html", context)


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


def product_detail(request, product_id):
    data = cartData(request)
    cartItems = data["cartItems"]

    product = Produto.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        sizes_in_cart = {item.size: item.quantity for item in CarrinhoItem.objects.filter(product=product, order__customer=request.user.cliente)}
    else:
        sizes_in_cart = {}

    sizes_available = [(size.tamanho, size.quantidade > sizes_in_cart.get(size.tamanho, 0)) for size in product.tamanhoproduto_set.all()]

    context = {
        "product": product, 
        "cartItems": cartItems, 
        "sizes_available": sizes_available
    }
    return render(request, "store/product_detail.html", context)