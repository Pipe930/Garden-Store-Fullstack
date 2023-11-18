from django.db import models
from apps.branchs.models import Branch, Post
from apps.products.models import Store, Product
from apps.users.models import Person
from uuid import uuid4

# Supplier Model
class Supplier(Person):

    id_supplier = models.BigAutoField(primary_key=True)

    class Meta:

        db_table = "supplier"
        verbose_name = "supplier"
        verbose_name_plural = "suppliers"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

# Grocer Model
class Grocer(Person):

    id_grocer = models.BigAutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:

        db_table = "grocer"
        verbose_name = "grocer"
        verbose_name_plural = "grocers"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

# Employee Model
class Employee(Person):

    id_employee = models.BigAutoField(primary_key=True)
    date_contract = models.DateField()
    salary = models.PositiveIntegerField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:

        db_table = "employee"
        verbose_name = "employee"
        verbose_name_plural = "employees"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

# Bill Model
class Bill(models.Model):

    id_bill = models.BigAutoField(primary_key=True)
    code_uuid = models.UUIDField(default=uuid4, unique=True)
    created = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    total_price = models.PositiveBigIntegerField()
    products = models.JSONField()
    total_quantity = models.PositiveBigIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    grocer = models.ForeignKey(Grocer, on_delete=models.CASCADE)

    class Meta:

        db_table = "bill"
        verbose_name = "bill"
        verbose_name_plural = "bills"

    def __str__(self) -> str:
        return f"{self.grocer.first_name} {self.grocer.last_name}"

# Office Guie Model
class DispatchGuide(models.Model):

    class DispatchGuieState(models.TextChoices):

        preparation = "PR"
        distribution = "RE"
        shipment = "EV"
        revision = "RV"
        stored = "AL"

    id_dispatch_guide = models.BigAutoField(primary_key=True)
    code_uuid = models.UUIDField(default=uuid4, unique=True)
    created = models.DateField(auto_now_add=True)
    dispatch_date = models.DateField(blank=True, null=True)
    deliver_date = models.DateField(blank=True, null=True)
    state = models.CharField(max_length=2, choices=DispatchGuieState.choices, default=DispatchGuieState.preparation)
    destination = models.CharField(max_length=255)
    grocer = models.ForeignKey(Grocer, on_delete=models.CASCADE)

    class Meta:

        db_table = "dispatchguide"
        verbose_name = "dispatchguide"
        verbose_name_plural = "dispatchguides"

    def __str__(self) -> str:
        return str(self.code)

# Office Product Model
class GuieProduct(models.Model):

    id_guie_product = models.BigAutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    office_guie = models.ForeignKey(DispatchGuide, on_delete=models.CASCADE)

    class Meta:

        db_table = "guieproduct"
        verbose_name = "guieproduct"
        verbose_name_plural = "guieproducts"

class OrderProduct(models.Model):

    id_order_product = models.BigAutoField(primary_key=True)
    code_uuid = models.UUIDField(default=uuid4, unique=True)
    created = models.DateField(auto_now_add=True)
    state = models.BooleanField(default=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    grocer = models.ForeignKey(Grocer, on_delete=models.CASCADE)

    class Meta:

        db_table = "orderproduct"
        verbose_name = "orderproduct"
        verbose_name_plural = "orderproducts"

class ProductsOrder(models.Model):

    id_products_order = models.BigAutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    order_product = models.ForeignKey(OrderProduct, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:

        db_table = "productsorder"
        verbose_name = "productsorder"
        verbose_name_plural = "productsorders"
