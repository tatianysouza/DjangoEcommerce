from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name if self.name else "Sem nome"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Produto(models.Model):
    GENEROS = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('U', 'Unissex'),
    )

    MARCAS = (
        ('O', 'Olympikus'),
        ('M', 'Mormaii'),
        ('C', 'Converse'),
        ('N', 'Nike'),
        ('A', 'Adidas'),
    )

    DEPARTAMENTOS = (
        ('E', 'Esporte'),
        ('C', 'Calçados'),
        ('A', 'Acessórios'),
        ('R', 'Corrida'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENEROS, blank=True)
    cor = models.CharField(max_length=200, null=True, blank=True)
    departamento_bs = models.CharField(max_length=1, null=True, choices=DEPARTAMENTOS, blank=True)
    indicado_para = models.CharField(max_length=200, null=True, blank=True)
    material = models.CharField(max_length=200, null=True, blank=True)
    material_interno = models.CharField(max_length=200, null=True, blank=True)
    altura_do_cano = models.CharField(max_length=200, null=True, blank=True)
    solado = models.CharField(max_length=200, null=True, blank=True)
    peso_do_produto = models.FloatField(blank=True, null=True)
    marca = models.CharField(max_length=1, choices=MARCAS,null=True, blank=True)
    importante = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

class TamanhoProduto(models.Model):
    TAMANHOS = (
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
        ('45', '45'),
    )

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tamanho = models.CharField(max_length=2, choices=TAMANHOS)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.produto.name} - {self.tamanho}'


class Carrinho(models.Model):
    customer = models.ForeignKey(
        Cliente, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        if self.complete:
            return f'{self.customer.name} - {self.transaction_id}'
        else:
            return f'{self.customer.name} - Carrinho'

    @property
    def shipping(self):
        return True


    @property
    def get_cart_total(self):
        orderitems = self.carrinhoitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.carrinhoitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    class Meta:
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinhos"


class CarrinhoItem(models.Model):
    product = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Carrinho, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    size = models.CharField(max_length=2, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.order is not None:
            if self.order.complete:
                return f'{self.order.customer.name} - {self.order.transaction_id}'
            else:
                return f'{self.order.customer.name} - Carrinho'
        else:
            return 'CarrinhoItem sem pedido associado'

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    class Meta:
        unique_together = ('product', 'order', 'size')
    class Meta:
        verbose_name = "Carrinho Item"
        verbose_name_plural = "Carrinho Itens"


class EnderecoEnvio(models.Model):
    customer = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Carrinho, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.name} - {self.address}'

    class Meta:
        verbose_name = "Endereço de Envio"
        verbose_name_plural = "Endereços de Envio"


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        try:
            Cliente.objects.get_or_create(
                user=instance, name=instance.username, email=instance.email
            )
        except Exception as e:
            print(f"Erro ao criar Cliente para o User {instance.username}: {str(e)}")


@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    pass

class Pedido(models.Model):
    customer = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f'{self.customer.name} - {self.transaction_id}'

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    product = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    size = models.CharField(max_length=2)

    def __str__(self):
        return f'{self.product.name} - {self.size} ({self.quantity})'

@receiver(post_save, sender=EnderecoEnvio)
def create_pedido(sender, instance, created, **kwargs):
    order = instance.order
    if order.complete:
        order_items_str = ', '.join([f'{item.product.name} ({item.quantity})' for item in order.carrinhoitem_set.all()])
        pedido = Pedido.objects.create(
            customer=order.customer,
            transaction_id=order.transaction_id,
            address=instance.address,
            city=instance.city,
            state=instance.state,
            zipcode=instance.zipcode,
            order_items=order_items_str,
        )
        for item in order.carrinhoitem_set.all():
            PedidoItem.objects.create(
                pedido=pedido,
                product=item.product,
                quantity=item.quantity,
                size=item.size,
            )
        order.carrinhoitem_set.all().delete()
        order.delete()
        