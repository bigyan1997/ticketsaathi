from django.contrib import admin
from .models import Route, Bus, Trip


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'operator', 'estimated_duration', 'is_active')
    list_filter = ('is_active', 'operator')
    search_fields = ('origin', 'destination', 'operator__company_name')


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_number', 'bus_type', 'total_seats', 'operator', 'is_active')
    list_filter = ('bus_type', 'is_active', 'operator')
    search_fields = ('name', 'registration_number', 'operator__company_name')


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('route', 'bus', 'departure_time', 'arrival_time', 'price', 'available_seats', 'status')
    list_filter = ('status', 'route__operator')
    search_fields = ('route__origin', 'route__destination', 'bus__name')
    ordering = ('departure_time',)
