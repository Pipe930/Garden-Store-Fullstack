from django.db import models
from os.path import join
import uuid
import hashlib
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
    title = models.CharField(max_length=255, unique=True)
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField()
    sold = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=40)
    image = models.ImageField(upload_to=nameImage)
    slug = models.SlugField(unique=True)
    aviable = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True, default="(Sin Descripcion)")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:

        db_table = "product"
        verbose_name = "product"
        verbose_name_plural = "products"

    def __str__(self) -> str:
        return self.title

# Function to define the slug of the product
def set_slug(sender, instance, *args, **kwargs):
    if instance.slug:
        return

    id = str(uuid.uuid4())
    instance.slug = slugify("{}-{}".format(
        instance.title, id
    ))

pre_save.connect(set_slug, sender = Product)
