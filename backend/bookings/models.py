from django.db import models
from django.conf import settings
from routes.models import Trip


class Booking(models.Model):
    """
    A passenger reserving one seat on a specific trip.
    One booking = one seat. For multiple seats, multiple bookings are created.
    """

    STATUS_CHOICES = [
        ('pending',   'Pending'),    # booking created, waiting for payment
        ('confirmed', 'Confirmed'),  # payment received, seat is locked
        ('cancelled', 'Cancelled'),  # booking was cancelled
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')

    seat_number = models.CharField(max_length=10)  # e.g. "12" or "A3"

    # Stored separately in case the account holder books for someone else
    passenger_name = models.CharField(max_length=150)
    passenger_phone = models.CharField(max_length=15)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Snapshot of the price at the time of booking
    # Stored here so price changes on the trip don't affect existing bookings
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-booked_at']
        # Prevent two people from booking the same seat on the same trip
        unique_together = ('trip', 'seat_number')

    def __str__(self):
        return f'Booking #{self.pk} — {self.passenger_name} on {self.trip}'
