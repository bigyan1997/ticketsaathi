from django.db import models
from bookings.models import Booking


class Payment(models.Model):
    """
    Records a payment transaction for a booking.
    One booking has one payment. If payment fails, a new attempt creates a new Payment record.
    """

    METHOD_CHOICES = [
        ('esewa',  'eSewa'),    # most popular in Nepal
        ('khalti', 'Khalti'),   # second most popular
        ('card',   'Card'),     # credit/debit card
        ('cash',   'Cash'),     # for walk-in / counter bookings
    ]

    STATUS_CHOICES = [
        ('pending',   'Pending'),    # payment initiated but not confirmed yet
        ('completed', 'Completed'),  # money received successfully
        ('failed',    'Failed'),     # payment attempt failed
        ('refunded',  'Refunded'),   # money was returned to the user
    ]

    # OneToOneField means one booking can only have one payment record
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')

    amount = models.DecimalField(max_digits=8, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # The reference ID returned by eSewa/Khalti after a transaction
    # Blank until the payment provider confirms the transaction
    transaction_id = models.CharField(max_length=200, blank=True)

    paid_at = models.DateTimeField(blank=True, null=True)  # set when status becomes 'completed'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']

    def __str__(self):
        return f'Payment #{self.pk} — {self.method} — {self.status} — Rs. {self.amount}'
