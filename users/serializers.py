from rest_framework import serializers
from users.models import User, Payment


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "email": {"required": False},
        }

    def update(self, instance: User, validated_data):  # Added type hint here
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        return super().update(instance, validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
