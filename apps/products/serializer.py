from rest_framework.serializers import ModelSerializer, StringRelatedField, Serializer, IntegerField, CharField, SerializerMethodField
from .models import Category, Product, Offer

# List Categories Serializer
class ListCategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ("id_category", "name_category")

# Offer Serializer
class OfferSerializer(ModelSerializer):

    class Meta:

        model = Offer
        fields = ("id_offer", "name_offer", "percentage_discount")

# List Products Serializer
class ListProductsSerializer(ModelSerializer):

    category = StringRelatedField()
    offer = OfferSerializer(many=False)
    image = SerializerMethodField(method_name="get_image")

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

    def get_image(self, product: Product):
        return product.image.url

class SearchProductSerialzer(Serializer):

    id_category = IntegerField()
    name_product = CharField(allow_blank=True)
