# Generated by Django 4.0.5 on 2024-01-22 20:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0019_produto_altura_do_cano_produto_departamento_bs_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="produto",
            name="cor",
            field=models.CharField(default="Desconhecido", max_length=200),
        ),
    ]
