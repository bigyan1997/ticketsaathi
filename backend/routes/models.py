from django.db import models
from operators.models import Operator


class Route(models.Model):
    """
    A fixed path between two cities operated by a bus company.
    Example: Kathmandu → Pokhara (operated by Greenline)
    One operator can have many routes.
    """

    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, related_name='routes')
    origin = models.CharField(max_length=100)       # e.g. "Kathmandu"
    destination = models.CharField(max_length=100)  # e.g. "Pokhara"

    # How long the journey takes, e.g. "6:30:00" = 6 hours 30 minutes
    estimated_duration = models.DurationField()

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Route'
        verbose_name_plural = 'Routes'
        ordering = ['origin', 'destination']

    def __str__(self):
        return f'{self.origin} → {self.destination} ({self.operator.company_name})'


class Bus(models.Model):
    """
    A physical bus owned by an operator.
    One operator can own many buses.
    """

    BUS_TYPES = [
        ('local',   'Local'),
        ('express', 'Express'),
        ('tourist', 'Tourist'),
        ('deluxe',  'Deluxe'),
    ]

    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, related_name='buses')
    name = models.CharField(max_length=100)                          # e.g. "Greenline 01"
    registration_number = models.CharField(max_length=50, unique=True)  # e.g. "BA 1 KHA 1234"
    bus_type = models.CharField(max_length=20, choices=BUS_TYPES, default='local')
    total_seats = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Bus'
        verbose_name_plural = 'Buses'
        ordering = ['operator', 'name']

    def __str__(self):
        return f'{self.name} ({self.registration_number})'


class Trip(models.Model):
    """
    A specific scheduled journey — a bus running a route on a particular date and time.
    Example: Greenline 01 running Kathmandu→Pokhara on 2026-05-20 at 07:00, Rs. 2500/seat.
    This is what passengers actually book.
    """

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='trips')
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='trips')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    # Price per seat in Nepali Rupees (e.g. 2500.00)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    # Decreases by 1 each time a seat is booked
    available_seats = models.PositiveIntegerField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    class Meta:
        verbose_name = 'Trip'
        verbose_name_plural = 'Trips'
        ordering = ['departure_time']

    def __str__(self):
        return f'{self.route} — {self.departure_time.strftime("%Y-%m-%d %H:%M")}'
