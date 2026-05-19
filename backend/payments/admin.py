from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'method', 'amount', 'status', 'transaction_id', 'paid_at')
    list_filter = ('status', 'method')
    search_fields = ('transaction_id', 'booking__passenger_name', 'booking__user__email')
    ordering = ('-created_at',)
