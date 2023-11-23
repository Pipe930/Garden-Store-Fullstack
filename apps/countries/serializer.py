from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import Commune, Region, Province

# List Region Serializer
class RegionSerializer(ModelSerializer):

    class Meta:

        model = Region
        fields = ("id_region", "name_region", "initials")

# List Province Serializer
class ProvinceSerializer(ModelSerializer):

    region = StringRelatedField()

    class Meta:

        model = Province
        fields = ("id_province", "name_province", "region")

# List Commune Serializer
class CommuneSerializer(ModelSerializer):

    province = StringRelatedField()

    class Meta:

        model = Commune
        fields = ("id_commune", "name_commune", "province")
