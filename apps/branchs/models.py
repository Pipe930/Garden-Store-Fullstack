from django.db import models
from apps.countries.models import Commune
from apps.products.models import Product

# Branch Model
class Branch(models.Model):

    id_branch = models.BigAutoField(primary_key=True)
    name_branch = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    capacity_ocuped = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=20, unique=True)
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
    name_post = models.CharField(max_length=20)

    class Meta:

        db_table = "post"
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self) -> str:
        return self.name_post

# Employee Model
class Employee(models.Model):

    class OrderWithdrawal(models.TextChoices):

        male = "masculino"
        female = "femenino"
        other = "otro"

    id_employee = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    birthday = models.DateField()
    salary = models.PositiveIntegerField()
    contract_date = models.DateField(auto_now_add=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:

        db_table = "employee"
        verbose_name = "employee"
        verbose_name_plural = "employees"

