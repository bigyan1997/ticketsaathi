from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """Factory for creating users. Called via User.objects.create_user(...)"""

    def create_user(self, phone_number, full_name='', password=None, **extra_fields):
        if not phone_number:
            raise ValueError('A phone number is required to create a user.')
        user = self.model(phone_number=phone_number, full_name=full_name, **extra_fields)
        user.set_password(password)  # hashes the password; None = no password (OTP users)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, full_name='', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone_number, full_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for Ticket Saathi.
    Users log in with phone number + OTP (not username/password).
    Replaces Django's built-in User completely.
    """

    # Phone number is the unique login identifier (like a username)
    phone_number = models.CharField(max_length=15, unique=True, db_index=True)

    # Email is optional — used mainly for Google OAuth login
    email = models.EmailField(blank=True, null=True, unique=True)

    full_name = models.CharField(max_length=150, blank=True)

    # OTP fields — set when SMS is sent, cleared after successful login
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    LANGUAGE_CHOICES = [('en', 'English'), ('ne', 'Nepali (नेपाली)')]
    preferred_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')

    # Role flags — a user can be both customer and operator
    is_customer = models.BooleanField(default=True)
    is_operator = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'  # Django uses this field to identify users
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.phone_number} ({self.full_name or "No name yet"})'

    def is_otp_valid(self, otp_code):
        """Returns True if the OTP exists, has not expired, and matches the given code."""
        if not self.otp or not self.otp_expiry:
            return False
        if timezone.now() > self.otp_expiry:
            return False
        return str(self.otp) == str(otp_code)

    def clear_otp(self):
        """Deletes the OTP after successful login so it cannot be reused."""
        self.otp = None
        self.otp_expiry = None
        self.save(update_fields=['otp', 'otp_expiry'])
