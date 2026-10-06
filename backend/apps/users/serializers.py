from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["uuid", "username", "email", "first_name", "last_name", "date_joined"]
        read_only_fields = ["uuid", "email", "date_joined"]


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = UserModel
        fields = ["username", "email", "password", "first_name", "last_name"]

    def validate(self, attrs):
        # Unsaved instance so UserAttributeSimilarityValidator can compare fields
        candidate = UserModel(
            username=attrs.get("username"),
            email=attrs.get("email"),
            first_name=attrs.get("first_name", ""),
            last_name=attrs.get("last_name", ""),
        )
        validate_password(attrs["password"], user=candidate)
        return attrs

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)
