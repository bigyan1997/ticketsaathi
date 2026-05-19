from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Used when a new user signs up."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password')

    def create(self, validated_data):
        # create_user hashes the password — never store plain text
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """Used for viewing and updating the logged-in user's profile."""

    class Meta:
        model = User
        fields = (
            'id', 'email', 'full_name', 'phone_number',
            'preferred_language', 'is_customer', 'is_operator', 'created_at',
        )
        # These fields cannot be changed by the user themselves
        read_only_fields = ('id', 'email', 'is_customer', 'is_operator', 'created_at')
