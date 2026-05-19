from rest_framework import serializers
from django.utils import timezone
from .models import Payment
from bookings.models import Booking


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Used when a passenger initiates a payment for their booking."""

    class Meta:
        model = Payment
        fields = ('booking', 'method')

    def validate_booking(self, booking):
        user = self.context['request'].user

        # Only the owner of the booking can pay for it
        if booking.user != user:
            raise serializers.ValidationError('You do not own this booking.')

        # Can't pay for a cancelled booking
        if booking.status == 'cancelled':
            raise serializers.ValidationError('This booking has been cancelled.')

        # Can't pay twice — check if a completed payment already exists
        if hasattr(booking, 'payment') and booking.payment.status == 'completed':
            raise serializers.ValidationError('This booking has already been paid.')

        return booking

    def create(self, validated_data):
        booking = validated_data['booking']

        # If a previous failed attempt exists, reuse it instead of creating a duplicate
        existing = Payment.objects.filter(booking=booking).first()
        if existing:
            existing.method = validated_data['method']
            existing.status = 'pending'
            existing.save(update_fields=['method', 'status'])
            return existing

        return Payment.objects.create(
            booking=booking,
            method=validated_data['method'],
            amount=booking.total_price,
        )


class PaymentConfirmSerializer(serializers.Serializer):
    """
    Used to confirm a payment after the user completes it on eSewa/Khalti.
    The frontend sends back the transaction_id provided by the payment gateway.
    """

    transaction_id = serializers.CharField(max_length=200)


class PaymentSerializer(serializers.ModelSerializer):
    """Read-only view of a payment."""

    booking_id = serializers.IntegerField(source='booking.id', read_only=True)

    class Meta:
        model = Payment
        fields = (
            'id', 'booking_id', 'amount', 'method',
            'status', 'transaction_id', 'paid_at', 'created_at',
        )
