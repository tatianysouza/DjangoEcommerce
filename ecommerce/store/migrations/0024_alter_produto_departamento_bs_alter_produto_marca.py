# Generated by Django 4.0.5 on 2024-01-24 18:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0023_alter_produto_departamento_bs_alter_produto_marca"),
    ]

    operations = [
        migrations.AlterField(
            model_name="produto",
            name="departamento_bs",
            field=models.CharField(
                blank=True,
                choices=[
                    ("E", "Esporte"),
                    ("C", "Calçados"),
                    ("A", "Acessórios"),
                    ("R", "Corrida"),
                ],
                max_length=1,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="produto",
            name="marca",
            field=models.CharField(
                blank=True,
                choices=[
                    ("O", "Olympikus"),
                    ("M", "Mormaii"),
                    ("C", "Converse"),
                    ("N", "Nike"),
                    ("A", "Adidas"),
                ],
                max_length=1,
                null=True,
            ),
        ),
    ]
