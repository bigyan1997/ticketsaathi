from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'passenger_name', 'trip', 'seat_number', 'status', 'total_price', 'booked_at')
    list_filter = ('status',)
    search_fields = ('passenger_name', 'passenger_phone', 'user__email')
    ordering = ('-booked_at',)
