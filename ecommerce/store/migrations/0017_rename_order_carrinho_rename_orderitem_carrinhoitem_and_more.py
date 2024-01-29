# Generated by Django 4.0.5 on 2024-01-21 19:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("store", "0016_remove_pedido_products_pedido_order_items_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Order",
            new_name="Carrinho",
        ),
        migrations.RenameModel(
            old_name="OrderItem",
            new_name="CarrinhoItem",
        ),
        migrations.RenameModel(
            old_name="Customer",
            new_name="Cliente",
        ),
        migrations.RenameModel(
            old_name="ShippingAddress",
            new_name="EnderecoEnvio",
        ),
        migrations.RenameModel(
            old_name="Product",
            new_name="Produto",
        ),
        migrations.AlterModelOptions(
            name="carrinho",
            options={"verbose_name": "Carrinho", "verbose_name_plural": "Carrinhos"},
        ),
        migrations.AlterModelOptions(
            name="carrinhoitem",
            options={
                "verbose_name": "Carrinho Item",
                "verbose_name_plural": "Carrinho Itens",
            },
        ),
        migrations.AlterModelOptions(
            name="cliente",
            options={"verbose_name": "Cliente", "verbose_name_plural": "Clientes"},
        ),
        migrations.AlterModelOptions(
            name="enderecoenvio",
            options={
                "verbose_name": "Endereço de Envio",
                "verbose_name_plural": "Endereços de Envio",
            },
        ),
        migrations.AlterModelOptions(
            name="pedido",
            options={"verbose_name": "Pedido", "verbose_name_plural": "Pedidos"},
        ),
        migrations.AlterModelOptions(
            name="produto",
            options={"verbose_name": "Produto", "verbose_name_plural": "Produtos"},
        ),
    ]
