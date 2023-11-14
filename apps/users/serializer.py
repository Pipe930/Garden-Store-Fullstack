from rest_framework.serializers import ModelSerializer, CharField, EmailField, Serializer, StringRelatedField
from .models import User, Subscription

# Serialized User Model
class CreateUserSerializer(ModelSerializer):

    class Meta:

        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "is_active",
            "is_staff",
        )
        extra_kwargs = {"password": {"write_only": True, "min_length": 8, "max_length": 16}}

    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)

        return user

# Serialized Subscription Model
class CreateSubscriptionSerializer(ModelSerializer):

    class Meta:

        model = Subscription
        fields = ["mount", "user"]

    def create(self, validated_data):

        subscription = Subscription.objects.create(**validated_data)

        return subscription

class ListSubscriptionSerializer(ModelSerializer):

    user = StringRelatedField()

    class Meta:

        model = Subscription
        fields = ["id_subscription", "created", "status", "mount", "user"]

# Send mail serializer
class MessageSerializer(Serializer):

    # Required attributes
    full_name = CharField(max_length=60)
    email = EmailField()
    message = CharField(max_length=255)

# Change Password Serializer
class ChangePasswordSerializer(Serializer):

    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = CharField(required=True)
    new_password = CharField(required=True)
