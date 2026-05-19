from rest_framework import serializers
from .models import Review
from bookings.models import Booking


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Used when a passenger leaves a review for a trip they completed."""

    class Meta:
        model = Review
        fields = ('trip', 'rating', 'comment')

    def validate(self, data):
        user = self.context['request'].user
        trip = data['trip']

        # Only passengers who actually took the trip can review it
        took_the_trip = Booking.objects.filter(
            user=user,
            trip=trip,
            status='confirmed',
        ).exists()

        if not took_the_trip:
            raise serializers.ValidationError(
                'You can only review a trip you have a confirmed booking for.'
            )

        # Prevent duplicate reviews (unique_together on the model also enforces this)
        if Review.objects.filter(user=user, trip=trip).exists():
            raise serializers.ValidationError('You have already reviewed this trip.')

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Review.objects.create(**validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    """Public view of a review — shows the reviewer's name and trip info."""

    reviewer_name = serializers.CharField(source='user.full_name', read_only=True)
    trip_origin = serializers.CharField(source='trip.route.origin', read_only=True)
    trip_destination = serializers.CharField(source='trip.route.destination', read_only=True)

    class Meta:
        model = Review
        fields = (
            'id', 'reviewer_name',
            'trip_origin', 'trip_destination',
            'rating', 'comment', 'created_at',
        )
