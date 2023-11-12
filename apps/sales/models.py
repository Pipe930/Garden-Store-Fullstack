from django.db import models
from apps.users.models import User
from apps.products.models import Product
from apps.countries.models import Commune
from apps.branchs.models import Branch
from uuid import uuid4

# Cart Model
class Cart(models.Model):

    id_cart = models.BigAutoField(primary_key=True)
    total = models.PositiveIntegerField(default=0)
    total_quantity = models.PositiveIntegerField(default=0)
    total_products = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:

        db_table = "cart"
        verbose_name = "cart"
        verbose_name_plural = "carts"

    def __str__(self) -> str:
        return self.user.username

# Items Model
class Items(models.Model):

    id_items = models.BigAutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")

    class Meta:

        db_table = "items"
        verbose_name = "item"
        verbose_name_plural = "items"

class Order(models.Model):

    class OrderWithdrawal(models.TextChoices):

        store_pickup = "Retiro en Tienda"
        home_delivery = "Envio a Domicilio"

    class OrderCondition(models.TextChoices):

        preparation = "PR"
        retire = "RE"
        canceled = "CA"
        delivered = "ET"

    id_order = models.BigAutoField(primary_key=True)
    code_uuid = models.UUIDField(default=uuid4, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=True)
    net_mount = models.PositiveIntegerField()
    iva_price = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    quantity_products = models.PositiveIntegerField()
    condition = models.CharField(max_length=2, choices=OrderCondition.choices, default=OrderCondition.preparation)
    withdrawal = models.CharField(max_length=20, choices=OrderWithdrawal.choices)
    direction = models.CharField(max_length=255, null=True, blank=True)
    num_deparment = models.PositiveSmallIntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commune = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:

        db_table = "order"
        verbose_name = "order"
        verbose_name_plural = "orders"

    def __str__(self) -> str:
        return str(self.code)

class OrderItem(models.Model):

    id_order_item = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name_product = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:

        db_table = "ordenitem"
        verbose_name = "ordenitem"
        verbose_name_plural = "ordenitems"

class Warranty(models.Model):

    id_warranty = models.BigAutoField(primary_key=True)
    code_uuid = models.UUIDField(default=uuid4, unique=True)
    created = models.DateField(auto_now_add=True)
    state = models.BooleanField(default=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:

        db_table = "warranty"
        verbose_name = "warranty"
        verbose_name_plural = "warranties"
