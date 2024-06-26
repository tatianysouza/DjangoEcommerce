# Generated by Django 4.0.5 on 2024-06-14 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0044_alter_produto_descricao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='departamento_bs',
            field=models.CharField(blank=True, choices=[('Esporte', 'Esporte'), ('Calçados', 'Calçados'), ('Acessorios', 'Acessórios'), ('Corrida', 'Corrida'), ('Futebol', 'Futebol')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='genero',
            field=models.CharField(blank=True, choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino'), ('Unissex', 'Unissex')], max_length=20),
        ),
        migrations.AlterField(
            model_name='produto',
            name='marca',
            field=models.CharField(blank=True, choices=[('Olympikus', 'Olympikus'), ('Mormaii', 'Mormaii'), ('Converse', 'Converse'), ('Nike', 'Nike'), ('Adidas', 'Adidas'), ('Puma', 'Puma'), ('Asics', 'Asics'), ('Mizuno', 'Mizuno'), ('Vans', 'Vans'), ('Fila', 'Fila')], max_length=20, null=True),
        ),
    ]
