from django.db import models
from os.path import join
import uuid
from datetime import datetime
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Category Model
class Category(models.Model):

    id_category = models.BigAutoField(primary_key=True)
    name_category = models.CharField(max_length=60, unique=True)

    class Meta:

        db_table = "category"
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name_category

# Offer Model
class Offer(models.Model):

    id_offer = models.BigAutoField(primary_key=True)
    name_offer = models.CharField(max_length=255)
    state = models.BooleanField(default=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    percentage_discount = models.PositiveSmallIntegerField()

    class Meta:

        db_table = "offer"
        verbose_name = "offer"
        verbose_name_plural = "offers"

    def __str__(self) -> str:
        return self.name_offer

# Function to name images
def nameImage(request, name_image):
    old_name = name_image
    current_date = datetime.now().strftime("%Y%m%d%H:%M:%S")
    name_image = "%s%s" % (current_date, old_name)
    return join("images/", name_image)

# Product Model
class Product(models.Model):

    id_product = models.BigAutoField(primary_key=True)
    name_product = models.CharField(max_length=255, unique=True)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to=nameImage)
    slug = models.SlugField(unique=True)
    aviable = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True, default="(Sin Descripcion)")
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:

        db_table = "product"
        verbose_name = "product"
        verbose_name_plural = "products"

    def __str__(self) -> str:
        return self.name_product

# Function to define the slug of the product
def set_slug(sender, instance, *args, **kwargs):
    if instance.slug:
        return

    id = str(uuid.uuid4())
    instance.slug = slugify("{}-{}".format(
        instance.name_product, id[:8]
    ))

pre_save.connect(set_slug, sender = Product)

# Store Model
class Store(models.Model):

    id_store = models.BigAutoField(primary_key=True)
    name_store = models.CharField(max_length=255, unique=True)
    direction = models.CharField(max_length=255)
    temperature = models.SmallIntegerField()
    capacity = models.PositiveBigIntegerField()
    ocupied_capacity = models.PositiveBigIntegerField(default=0)

    class Meta:

        db_table = "store"
        verbose_name = "store"
        verbose_name_plural = "cellars"

    def __str__(self) -> str:
        return self.name_store

# Product Store Model
class StoreProduct(models.Model):

    id_store_product = models.BigAutoField(primary_key=True)
    quantity = models.PositiveBigIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:

        db_table = "storeproduct"
        verbose_name = "storeproduct"
        verbose_name_plural = "storeproducts"

