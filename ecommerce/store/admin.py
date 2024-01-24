from django.contrib import admin
from .models import *
class TamanhoProdutoInline(admin.TabularInline):
    model = TamanhoProduto
    extra = 1
class ProdutoAdmin(admin.ModelAdmin):
    inlines = [TamanhoProdutoInline]

admin.site.register(Cliente)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Carrinho)
admin.site.register(CarrinhoItem)
admin.site.register(EnderecoEnvio)
admin.site.register(Pedido)
