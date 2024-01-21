from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Cliente)
admin.site.register(Produto)
admin.site.register(Carrinho)
admin.site.register(CarrinhoItem)
admin.site.register(EnderecoEnvio)
admin.site.register(Pedido)
