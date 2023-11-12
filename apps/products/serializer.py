from rest_framework.serializers import ModelSerializer
from .models import Category, Product, Offer

# List Categories Serializer
class ListCategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["id_category", "name_category"]

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
