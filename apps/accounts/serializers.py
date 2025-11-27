from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = (
    get_user_model()
)  # dynamically fetches the user model (whether default or custom)


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="User's email address")
    password = serializers.CharField(help_text="User's password", write_only=True)
    first_name = serializers.CharField(help_text="User's first name")
    last_name = serializers.CharField(help_text="User's last name")

    def validate_email(self, value):
        """Check if email already exists."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")
        read_only_fields = ["email"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer to add user data to the token response."""

    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)
    #     print("SERIALIZER TOKEN", token)

    #     # Add custom claims
    #     token["email"] = user.email
    #     token["first_name"] = user.first_name
    #     token["last_name"] = user.last_name
    #     print("AFTER", token)
    #     return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add user data to response
        data["user"] = CustomUserSerializer(self.user).data

        return data
