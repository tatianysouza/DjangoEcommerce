# Generated by Django 4.0.5 on 2024-01-28 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0030_remove_carrinhoitem_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carrinho",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.cliente",
            ),
        ),
        migrations.AlterField(
            model_name="carrinhoitem",
            name="order",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.carrinho",
            ),
        ),
    ]
