from django.db import models
from apps.countries.models import Commune
from apps.products.models import Product

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
