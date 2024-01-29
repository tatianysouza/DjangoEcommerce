# Generated by Django 4.0.5 on 2024-01-21 18:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0012_pedido_address_pedido_city_pedido_state_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pedido",
            name="order",
        ),
        migrations.AddField(
            model_name="pedido",
            name="transaction_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
