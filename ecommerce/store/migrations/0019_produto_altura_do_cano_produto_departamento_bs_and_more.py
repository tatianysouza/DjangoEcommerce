# Generated by Django 4.0.5 on 2024-01-22 20:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0018_remove_produto_digital"),
    ]

    operations = [
        migrations.AddField(
            model_name="produto",
            name="altura_do_cano",
            field=models.CharField(default="Desconhecido", max_length=200),
        ),
        migrations.AddField(
            model_name="produto",
            name="departamento_bs",
            field=models.CharField(default="Desconhecido", max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="produto",
            name="genero",
            field=models.CharField(
                choices=[("M", "Masculino"), ("F", "Feminino"), ("U", "Unissex")],
                default="U",
                max_length=1,
            ),
        ),
        migrations.AddField(
            model_name="produto",
            name="indicado_para",
            field=models.CharField(default="Desconhecido", max_length=200),
        ),
        migrations.AddField(
            model_name="produto",
            name="marca",
            field=models.CharField(default="Desconhecido", max_length=200),
        ),
        migrations.AddField(
            model_name="produto",
            name="material",
            field=models.CharField(default="Desconhecido", max_length=200),
        ),
        migrations.AddField(
            model_name="produto",
            name="material_interno",
            field=models.CharField(default="Desconhecido", max_length=200),
        ),
        migrations.AddField(
            model_name="produto",
            name="peso_do_produto",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="produto",
            name="solado",
            field=models.CharField(default="Desconhecido", max_length=200),
        ),
    ]
