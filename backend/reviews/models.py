from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from routes.models import Trip


class Review(models.Model):
    """
    A rating and comment left by a passenger after completing a trip.
    A user can only review a trip once.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='reviews')

    # Rating must be between 1 and 5
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        # One review per user per trip
        unique_together = ('user', 'trip')

    def __str__(self):
        return f'{self.user.email} — {self.trip} — {self.rating}★'
