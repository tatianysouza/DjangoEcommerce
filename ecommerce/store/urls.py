from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.store, name="store"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path("search_results/", views.search_results, name="search_results"),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="store/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="store"), name="logout"),
    path("register/", views.register, name="register"),
    path('products/<str:category>/', views.products, name='products'),
]
