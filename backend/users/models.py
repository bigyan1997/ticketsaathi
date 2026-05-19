from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """Factory for creating users. Called via User.objects.create_user(...)"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('An email address is required.')
        email = self.normalize_email(email)  # lowercases the domain part (e.g. User@Gmail.COM → User@gmail.com)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for Ticket Saathi.
    Users log in with email + password, or via Google OAuth.
    """

    # Email is the unique login identifier
    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=150, blank=True)

    # Phone number is optional — useful for contact/notifications later
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)

    LANGUAGE_CHOICES = [('en', 'English'), ('ne', 'Nepali (नेपाली)')]
    preferred_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')

    # Role flags — a user can be both customer and operator
    is_customer = models.BooleanField(default=True)
    is_operator = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'  # Django uses this field to identify users
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.email} ({self.full_name or "No name yet"})'
