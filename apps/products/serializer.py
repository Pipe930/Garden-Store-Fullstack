from rest_framework.serializers import ModelSerializer, StringRelatedField, SerializerMethodField
from .models import Category, Product, Offer
from .discount import discount

# List Categories Serializer
class ListCategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["id_category", "name_category"]

# Create and Update Categories Serializer
class CreateUpdateCategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["name_category"]

    def create(self, validated_data):

        category = Category.objects.create(**validated_data)

        return category

    def update(self, instance, validated_data):

        instance.name_category = validated_data.get("name_category", instance.name_category)
        instance.save()

        return instance

class OfferSerializer(ModelSerializer):

    class Meta:

        model = Offer
        fields = ["id_offer", "name_offer", "discount"]

# List Products Serializer
class ListProductsSerializer(ModelSerializer):

    category = StringRelatedField()
    offer = OfferSerializer(many=False)

    class Meta:

        model = Product
        fields = [
            "id_product",
            "name_product",
            "price",
            "discount_price",
            "stock",
            "image",
            "slug",
            "aviable",
            "created",
            "description",
            "category",
            "offer"]

# Create and Update Products Serializer
class CreateUpdateProductSerializer(ModelSerializer):

    class Meta:

        model = Product
        exclude = ("id_product", "slug", "created", "aviable", "discount_price")

    def create(self, validated_data):

        try:
            if validated_data["offer"] is not None:
                discount_price = discount(product.price, product.offer.discount)
        except KeyError:
            discount_price = 0

        product = Product.objects.create(discount_price=discount_price,**validated_data)

        return product

    def update(self, instance, validated_data):

        try:
            if validated_data["offer"] is not None:
                discount_price = discount(instance.price, instance.offer.discount)
        except KeyError:
            discount_price = 0

        instance.name_product = validated_data.get("name_product", instance.name_product)
        instance.price = validated_data.get("price", instance.price)
        instance.stock = validated_data.get("stock", instance.stock)
        instance.image = validated_data.get("image", instance.image)
        instance.description = validated_data.get("description", instance.description)
        instance.category = validated_data.get("category", instance.category)
        instance.offer = validated_data.get("offer", instance.offer)
        instance.discount_price = discount_price

        instance.save()

        return instance
