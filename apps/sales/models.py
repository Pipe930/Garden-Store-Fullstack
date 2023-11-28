from django.db import models
from apps.products.models import Product
from apps.countries.models import Commune
from apps.branchs.models import Branch
from uuid import uuid4
from django.conf import settings
User = settings.AUTH_USER_MODEL

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

class Voucher(models.Model):

    class OrderWithdrawal(models.TextChoices):

        store_pickup = "Retiro en Tienda"
        home_delivery = "Envio a Domicilio"

    class OrderCondition(models.TextChoices):

        preparation = "PR"
        retire = "RE"
        shipped = "EV"
        canceled = "CA"
        delivered = "ET"

    id_voucher = models.BigAutoField(primary_key=True)
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

        db_table = "voucher"
        verbose_name = "voucher"
        verbose_name_plural = "vouchers"

    def __str__(self) -> str:
        return str(self.code)

class VoucherItem(models.Model):

    id_voucher_item = models.BigAutoField(primary_key=True)
    name_product = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)

    class Meta:

        db_table = "voucheritem"
        verbose_name = "voucheritem"
        verbose_name_plural = "voucheritems"

class Warranty(models.Model):

    id_warranty = models.BigAutoField(primary_key=True)
    code_uuid = models.UUIDField(default=uuid4, unique=True)
    created = models.DateField(auto_now_add=True)
    state = models.BooleanField(default=True)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:

        db_table = "warranty"
        verbose_name = "warranty"
        verbose_name_plural = "warranties"
