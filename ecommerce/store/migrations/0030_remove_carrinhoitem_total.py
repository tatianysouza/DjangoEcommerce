# Generated by Django 4.0.5 on 2024-01-25 20:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0029_carrinhoitem_total"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="carrinhoitem",
            name="total",
        ),
    ]
