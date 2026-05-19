from rest_framework import serializers
from .models import Operator


class OperatorSerializer(serializers.ModelSerializer):
    """Used to view and update an operator's company profile."""

    # Show the user's email so the frontend can display who owns this profile
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Operator
        fields = (
            'id', 'slug', 'user_email', 'company_name', 'registration_number',
            'logo', 'description', 'is_verified', 'created_at',
        )
        # Only an admin can flip is_verified; slug and created_at are automatic
        read_only_fields = ('id', 'slug', 'user_email', 'is_verified', 'created_at')


class ApplyOperatorSerializer(serializers.ModelSerializer):
    """Used when a user applies to become an operator for the first time."""

    class Meta:
        model = Operator
        fields = ('company_name', 'registration_number', 'logo', 'description')

    def create(self, validated_data):
        # Link the new operator profile to the logged-in user
        user = self.context['request'].user
        operator = Operator.objects.create(user=user, **validated_data)

        # Mark the user as an operator so permissions work
        user.is_operator = True
        user.save(update_fields=['is_operator'])

        return operator
