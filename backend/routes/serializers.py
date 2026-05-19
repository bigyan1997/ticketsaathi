from rest_framework import serializers
from .models import Route, Bus, Trip


class RouteSerializer(serializers.ModelSerializer):
    """Public view of a route — shows the operator's company name."""

    operator_name = serializers.CharField(source='operator.company_name', read_only=True)

    class Meta:
        model = Route
        fields = ('id', 'slug', 'operator_name', 'origin', 'destination', 'estimated_duration', 'is_active')


class RouteCreateSerializer(serializers.ModelSerializer):
    """Used by an operator to create a new route. Operator is set automatically."""

    class Meta:
        model = Route
        fields = ('origin', 'destination', 'estimated_duration')

    def create(self, validated_data):
        # Attach the operator profile of the logged-in user
        operator = self.context['request'].user.operator_profile
        return Route.objects.create(operator=operator, **validated_data)


class BusSerializer(serializers.ModelSerializer):
    """Used by an operator to list, create, and update their buses."""

    class Meta:
        model = Bus
        fields = ('id', 'name', 'registration_number', 'bus_type', 'total_seats', 'is_active')

    def create(self, validated_data):
        # Attach the operator profile of the logged-in user
        operator = self.context['request'].user.operator_profile
        return Bus.objects.create(operator=operator, **validated_data)


class TripSerializer(serializers.ModelSerializer):
    """Public view of a trip — includes route and bus details so passengers see everything."""

    origin = serializers.CharField(source='route.origin', read_only=True)
    destination = serializers.CharField(source='route.destination', read_only=True)
    operator_name = serializers.CharField(source='route.operator.company_name', read_only=True)
    bus_name = serializers.CharField(source='bus.name', read_only=True)
    bus_type = serializers.CharField(source='bus.bus_type', read_only=True)

    class Meta:
        model = Trip
        fields = (
            'id', 'slug', 'origin', 'destination', 'operator_name',
            'bus_name', 'bus_type',
            'departure_time', 'arrival_time',
            'price', 'available_seats', 'status',
        )


class TripCreateSerializer(serializers.ModelSerializer):
    """Used by an operator to schedule a new trip."""

    class Meta:
        model = Trip
        fields = ('route', 'bus', 'departure_time', 'arrival_time', 'price', 'available_seats')

    def validate(self, data):
        # Make sure arrival is after departure
        if data['arrival_time'] <= data['departure_time']:
            raise serializers.ValidationError('Arrival time must be after departure time.')
        return data
