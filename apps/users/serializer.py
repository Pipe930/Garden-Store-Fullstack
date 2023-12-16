from rest_framework.serializers import ModelSerializer, StringRelatedField, Serializer, CharField, EmailField
from .models import User, Subscription
from djoser.serializers import UserCreateSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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

class CustomTokenObtainSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):

        data = super().validate(attrs)

        obj = self.user

        data.update({
            "username": obj.username,
            "is_staff": obj.is_staff,
            "is_superuser": obj.is_superuser
        })

        return data

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

# Send mail serializer
class MessageSerializer(Serializer):

    # Required attributes
    full_name = CharField(max_length=60)
    email = EmailField()
    message = CharField(max_length=255)
