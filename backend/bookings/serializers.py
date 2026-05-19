from rest_framework import serializers
from .models import Booking
from routes.models import Trip


class BookingCreateSerializer(serializers.ModelSerializer):
    """Used when a passenger books a seat on a trip."""

    class Meta:
        model = Booking
        fields = ('trip', 'seat_number', 'passenger_name', 'passenger_phone')

    def validate(self, data):
        trip = data['trip']

        # Check the trip is still accepting bookings
        if trip.status != 'scheduled':
            raise serializers.ValidationError('This trip is no longer available for booking.')

        # Check there are seats left
        if trip.available_seats <= 0:
            raise serializers.ValidationError('No seats available on this trip.')

        # Check the seat is not already taken
        if Booking.objects.filter(trip=trip, seat_number=data['seat_number']).exists():
            raise serializers.ValidationError(f'Seat {data["seat_number"]} is already booked.')

        return data

    def create(self, validated_data):
        trip = validated_data['trip']

        # Lock in the price at the moment of booking
        validated_data['total_price'] = trip.price
        validated_data['user'] = self.context['request'].user

        # Reduce the available seat count by 1
        trip.available_seats -= 1
        trip.save(update_fields=['available_seats'])

        return Booking.objects.create(**validated_data)


class BookingSerializer(serializers.ModelSerializer):
    """Used to display a booking — includes trip info so the passenger sees full details."""

    trip_origin = serializers.CharField(source='trip.route.origin', read_only=True)
    trip_destination = serializers.CharField(source='trip.route.destination', read_only=True)
    trip_departure = serializers.DateTimeField(source='trip.departure_time', read_only=True)
    operator_name = serializers.CharField(source='trip.route.operator.company_name', read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id', 'trip_origin', 'trip_destination', 'trip_departure', 'operator_name',
            'seat_number', 'passenger_name', 'passenger_phone',
            'status', 'total_price', 'booked_at',
        )
