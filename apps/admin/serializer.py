from apps.products.models import Category, Product, Offer
from rest_framework.serializers import ModelSerializer, StringRelatedField
from apps.products.discount import discount

# List Categories Serializer
class ListCategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ("id_category", "name_category")

# Create and Update Categories Serializer
class CreateUpdateCategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ("name_category",)

class OfferSerializer(ModelSerializer):

    class Meta:

        model = Offer
        fields = ("id_offer", "name_offer", "percentage_discount")

# List Products Serializer
class ListProductsSerializer(ModelSerializer):

    category = StringRelatedField()
    offer = OfferSerializer(many=False)

    class Meta:

        model = Product
        fields = (
            "id_product",
            "title",
            "price",
            "discount_price",
            "stock",
            "brand",
            "sold",
            "image",
            "slug",
            "aviable",
            "created",
            "description",
            "category",
            "offer")

# Create and Update Products Serializer
class CreateUpdateProductSerializer(ModelSerializer):

    class Meta:

        model = Product
        exclude = ("id_product", "sold", "slug", "created", "aviable", "discount_price", "stock")

    def create(self, validated_data):

        try:
            price = validated_data["price"]
            offer = validated_data["offer"]

            if offer is not None:
                discount_price = discount(price, offer.percentage_discount)
        except KeyError:
            discount_price = 0

        product = Product.objects.create(discount_price=discount_price,**validated_data)

        return product

    def update(self, instance, validated_data):

        try:
            offer = validated_data["offer"]

            if offer is not None:
                discount_price = discount(instance.price, offer.percentage_discount)
                instance.discount_price = discount_price
                instance.offer = validated_data.get("offer", instance.offer)
            else:
                instance.offer = None

        except KeyError:
            instance.offer = None
            discount_price = 0

        instance.title = validated_data.get("title", instance.title)
        instance.price = validated_data.get("price", instance.price)
        instance.image = validated_data.get("image", instance.image)
        instance.brand = validated_data.get("brand", instance.brand)
        instance.description = validated_data.get("description", instance.description)
        instance.category = validated_data.get("category", instance.category)

        instance.save()

        return instance


# List Offers Serializer
class ListOfferSerializer(ModelSerializer):

    class Meta:
        model = Offer
        fields = ("id_offer", "name_offer", "state", "start_date", "end_date", "percentage_discount")

# Create and Update Offer Serializer
class CreateUpdateOfferSerializer(ModelSerializer):

    class Meta:
        model = Offer
        fields = ("name_offer", "end_date", "percentage_discount")
