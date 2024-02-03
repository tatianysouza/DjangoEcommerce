from django.contrib import admin
from .models import *


class TamanhoProdutoInline(admin.TabularInline):
    model = TamanhoProduto
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    inlines = [TamanhoProdutoInline]


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 1


class PedidoAdmin(admin.ModelAdmin):
    inlines = [PedidoItemInline]


admin.site.register(Cliente)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Carrinho)
admin.site.register(CarrinhoItem)
admin.site.register(EnderecoEnvio)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(CarouselImage)
