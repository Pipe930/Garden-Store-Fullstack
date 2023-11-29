from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import User, Subscription
from djoser.serializers import UserCreateSerializer

# Serialized User Model
class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "is_active"
        )

# Serialized Subscription Model
class CreateSubscriptionSerializer(ModelSerializer):

    class Meta:

        model = Subscription
        fields = ("mount", "user")

class ListSubscriptionSerializer(ModelSerializer):

    user = StringRelatedField()

    class Meta:

        model = Subscription
        fields = ("id_subscription", "created", "status", "mount", "user")
