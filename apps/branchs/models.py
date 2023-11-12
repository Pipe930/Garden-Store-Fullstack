from django.db import models
from apps.countries.models import Commune
from apps.products.models import Product
from apps.orders.models import Grocer
from apps.users.models import Person
from uuid import uuid4

# Branch Model
class Branch(models.Model):

    id_branch = models.BigAutoField(primary_key=True)
    name_branch = models.CharField(max_length=255, unique=True)
    direction = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255, unique=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)

    class Meta:

        db_table = "branch"
        verbose_name = "branch"
        verbose_name_plural = "branchoffices"

    def __str__(self) -> str:
        return self.name_branch

# Product Branch Model
class ProductBranch(models.Model):

    id_product_branch = models.BigAutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:

        db_table = "productbranch"
        verbose_name = "productbranch"
        verbose_name_plural = "productbranchoffices"

# Post Model
class Post(models.Model):

    id_post = models.BigAutoField(primary_key=True)
    name_post = models.CharField(max_length=60)

    class Meta:

        db_table = "post"
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self) -> str:
        return self.name_post

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
