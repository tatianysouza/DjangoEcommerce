# Generated by Django 4.0.5 on 2024-01-22 21:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0021_produto_importante_alter_produto_altura_do_cano_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="produto",
            name="altura_do_cano",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="produto",
            name="cor",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="produto",
            name="genero",
            field=models.CharField(
                blank=True,
                choices=[("M", "Masculino"), ("F", "Feminino"), ("U", "Unissex")],
                max_length=1,
            ),
        ),
        migrations.AlterField(
            model_name="produto",
            name="indicado_para",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="produto",
            name="marca",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="produto",
            name="material",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="produto",
            name="material_interno",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="produto",
            name="peso_do_produto",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="produto",
            name="solado",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
