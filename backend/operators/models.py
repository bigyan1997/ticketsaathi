from django.db import models
from django.conf import settings


class Operator(models.Model):
    """
    A bus company registered on Ticket Saathi.
    Every operator has a User account for logging in, plus this profile
    with their company details. An admin must verify them before they
    can create routes.
    """

    # One user account per operator (deleting the user also deletes this profile)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='operator_profile'
    )

    company_name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='operators/logos/', blank=True, null=True)
    description = models.TextField(blank=True)

    # Admin flips this to True after checking the company is legitimate
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Operator'
        verbose_name_plural = 'Operators'
        ordering = ['-created_at']

    def __str__(self):
        return self.company_name
