from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cookieCart, cartData, guestOrder

from django.contrib.auth.models import User

from django.core.validators import validate_email
from django.core.exceptions import ValidationError


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

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/cart.html", context)


def checkout(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/checkout.html", context)


def updateItem(request):
    data = json.loads(request.body.decode("utf-8"))
    productId = data["productId"]
    action = data["action"]

    print("Action:", action)
    print("productId:", productId)

    customer = request.user.cliente
    product = Produto.objects.get(id=productId)
    order, created = Carrinho.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = CarrinhoItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("item was added", safe=False)


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
    context = {"product": product, "cartItems": cartItems}
    return render(request, "store/product_detail.html", context)
