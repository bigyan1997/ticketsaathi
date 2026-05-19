# users/models.py
#
# This file defines what a "User" looks like in our database.
# In Nepal, people log in using their PHONE NUMBER + OTP (one-time password sent via SMS).
# They do NOT use a username and password like most western apps.
#
# Django has its own built-in User model (username + password).
# We are REPLACING it entirely with our own custom version.
# We told Django about this replacement in settings.py:
#   AUTH_USER_MODEL = 'users.User'

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────

# These come built into Python — no installation needed.
from django.utils import timezone   # For getting the current time (used in OTP expiry)

# These come with Django — they are the building blocks for custom user models.
from django.db import models

# AbstractBaseUser gives our model:
#   - password field (with hashing — stores passwords securely, never as plain text)
#   - last_login field (when did this user last log in?)
#   - is_active field (can this user log in at all?)
# We "inherit" these fields without having to write them ourselves.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# ─────────────────────────────────────────────────────────────────────────────
# USER MANAGER
# ─────────────────────────────────────────────────────────────────────────────

# A "Manager" is like a helper class that knows HOW to create users.
# Django's default manager creates users with username + password.
# We write our own manager to create users with phone_number instead.
#
# Think of it as: the Manager is the FACTORY, the User model is the PRODUCT.
# When you call User.objects.create_user(...), it goes through this Manager.

class UserManager(BaseUserManager):

    def create_user(self, phone_number, full_name='', password=None, **extra_fields):
        """
        Creates a normal user (customer or operator).
        This is called when someone registers on the website.

        phone_number  → the unique identifier for this user (like a username)
        full_name     → their real name
        password      → optional — our users log in with OTP, not passwords
        **extra_fields→ any other fields passed in (like email, preferred_language)
        """

        # Make sure a phone number was provided — we cannot create a user without one.
        # If someone calls create_user() without a phone number, raise an error immediately.
        if not phone_number:
            raise ValueError('A phone number is required to create a user.')

        # Save the user to the database and return the user object.
        # set_password() hashes the password so it is never stored as plain text.
        # If password is None (most of our users), no password is set — they use OTP.
        user = self.model(
            phone_number=phone_number,
            full_name=full_name,
            **extra_fields  # spreads any extra keyword arguments into the model
        )
        user.set_password(password)  # safely hash the password (or set unusable if None)
        user.save(using=self._db)    # save to the database (self._db is the default database)
        return user

    def create_superuser(self, phone_number, full_name='', password=None, **extra_fields):
        """
        Creates a superuser (admin).
        This is called when you run: python manage.py createsuperuser
        The superuser can log into /admin/ and manage everything.

        Superusers MUST have a password because they log into /admin/ with password.
        """

        # Force these fields to be True for superusers.
        # is_staff=True   → can log into the /admin/ panel
        # is_superuser=True → has ALL permissions in the system (bypasses all checks)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Safety check — make sure no one accidentally creates a superuser
        # with is_staff=False or is_superuser=False.
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Reuse create_user() — no need to repeat the same logic.
        return self.create_user(phone_number, full_name, password, **extra_fields)


# ─────────────────────────────────────────────────────────────────────────────
# USER MODEL
# ─────────────────────────────────────────────────────────────────────────────

class User(AbstractBaseUser, PermissionsMixin):
    """
    The main User model for Ticket Saathi.

    This replaces Django's built-in User completely.
    Every person who uses the app — customer, operator, or admin — is stored here.

    AbstractBaseUser gives us: password, last_login, is_active
    PermissionsMixin gives us: is_superuser, groups, user_permissions
                               (these are needed for the /admin/ panel to work)
    """

    # ── Phone Number ─────────────────────────────────────────────────────────
    # This is the PRIMARY way users identify themselves on Ticket Saathi.
    # In Nepal, everyone has a phone. Not everyone has an email.
    #
    # max_length=15  → international standard for phone numbers (e.g., +977-9841234567)
    # unique=True    → NO two users can have the same phone number
    # db_index=True  → creates a database index for fast lookup (important for search speed)
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        db_index=True,
        verbose_name='Phone Number'
    )

    # ── Email ─────────────────────────────────────────────────────────────────
    # Optional — used mainly for Google OAuth login (Google provides an email).
    # blank=True → form validation allows this field to be empty
    # null=True  → database stores NULL (empty) if not provided
    # unique=True with null=True → two users CAN both have null email,
    #                              but no two users can share a real email address.
    email = models.EmailField(
        blank=True,
        null=True,
        unique=True,
        verbose_name='Email Address'
    )

    # ── Full Name ─────────────────────────────────────────────────────────────
    # The user's real name (e.g., "Ram Bahadur Shrestha").
    # blank=True → it is optional when creating a user (e.g., right after OTP verification)
    full_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Full Name'
    )

    # ── OTP (One-Time Password) ───────────────────────────────────────────────
    # The 6-digit code we send via SMS to verify the user's phone number.
    # Example: "482917"
    #
    # blank=True, null=True → most of the time this is empty (only set when OTP is sent)
    # We store it temporarily — once verified, we clear it from the database.
    otp = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        verbose_name='OTP Code'
    )

    # ── OTP Expiry ────────────────────────────────────────────────────────────
    # The exact date and time when the OTP stops being valid.
    # We set this to "now + 10 minutes" when we send the OTP.
    # When verifying: if timezone.now() > otp_expiry → OTP has expired → reject it.
    #
    # DateTimeField → stores both date AND time (e.g., 2026-05-19 14:30:00)
    otp_expiry = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='OTP Expiry Time'
    )

    # ── Preferred Language ────────────────────────────────────────────────────
    # Whether the user wants the app in English or Nepali.
    # 'en' = English (default)
    # 'ne' = Nepali (नेपाली)
    #
    # choices= limits the database to only these two values.
    # This prevents someone from setting language to "xyz" accidentally.
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ne', 'Nepali (नेपाली)'),
    ]
    preferred_language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='en',
        verbose_name='Preferred Language'
    )

    # ── Role Flags ────────────────────────────────────────────────────────────
    # These flags tell us what TYPE of user this person is.
    # A user can be both a customer AND an operator (e.g., a bus owner who also books tickets).
    #
    # is_customer → can search trips, book seats, make payments, view tickets
    # is_operator → can manage routes, buses, trips; view passenger lists
    is_customer = models.BooleanField(
        default=True,  # everyone is a customer by default when they register
        verbose_name='Is Customer'
    )
    is_operator = models.BooleanField(
        default=False, # not an operator by default — admin approves operators separately
        verbose_name='Is Operator'
    )

    # ── Django Admin Flags (from PermissionsMixin / AbstractBaseUser) ─────────
    # is_active  → can this user log in? Set to False to "ban" a user without deleting them.
    # is_staff   → can this user access the /admin/ panel? (True for superusers and staff)
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is Active'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Is Staff (Admin Access)'
    )

    # ── Timestamps ────────────────────────────────────────────────────────────
    # auto_now_add=True → Django automatically sets this to the current time
    #                     when the user is FIRST created. Never changes after that.
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Account Created At'
    )

    # ── Manager ───────────────────────────────────────────────────────────────
    # Attach our custom UserManager to this model.
    # Now when you write:  User.objects.create_user(...)
    # Django uses OUR manager, not the default one.
    objects = UserManager()

    # ── Login Field ───────────────────────────────────────────────────────────
    # USERNAME_FIELD tells Django: "This is what uniquely identifies a user."
    # By default Django uses 'username'. We change it to 'phone_number'.
    # This affects:
    #   - What field is asked for when logging into /admin/
    #   - What field JWT tokens use to look up the user
    USERNAME_FIELD = 'phone_number'

    # REQUIRED_FIELDS: extra fields asked for when running "python manage.py createsuperuser"
    # phone_number is already required (it's the USERNAME_FIELD), so we leave this empty.
    # If we added 'full_name' here, the command would ask for it interactively.
    REQUIRED_FIELDS = []

    # ── Meta ──────────────────────────────────────────────────────────────────
    # Meta = extra information about this model (not a database column).
    class Meta:
        verbose_name = 'User'           # singular label used in /admin/
        verbose_name_plural = 'Users'   # plural label used in /admin/
        ordering = ['-created_at']      # default sort: newest users appear first

    # ── String Representation ─────────────────────────────────────────────────
    # __str__ controls what you see when Django prints a user object.
    # For example, in the admin panel or in error messages.
    # Without this, you'd see: <User object (1)>
    # With this, you see:       9841234567 (Ram Bahadur Shrestha)
    def __str__(self):
        return f'{self.phone_number} ({self.full_name or "No name yet"})'

    # ── Helper Methods ────────────────────────────────────────────────────────

    def is_otp_valid(self, otp_code):
        """
        Checks if the OTP the user submitted is correct AND still within the 10-minute window.

        Returns True  → OTP is correct and not expired → allow login
        Returns False → OTP is wrong or expired       → reject login

        How to use:
            if user.is_otp_valid('482917'):
                # create JWT token and log them in
        """
        # Check 1: Does an OTP even exist for this user right now?
        if not self.otp or not self.otp_expiry:
            return False

        # Check 2: Has the OTP expired?
        # timezone.now() gives the current time in UTC (matches what we stored).
        if timezone.now() > self.otp_expiry:
            return False

        # Check 3: Does the code the user entered match what we stored?
        # We compare as strings because OTPs starting with 0 (e.g., "012345")
        # would lose the leading zero if treated as integers.
        return str(self.otp) == str(otp_code)

    def clear_otp(self):
        """
        Deletes the OTP after it has been used successfully.
        This is a security measure — used OTPs should not be reusable.

        How to use:
            if user.is_otp_valid(code):
                user.clear_otp()   # delete it immediately after login
                # then issue JWT tokens
        """
        self.otp = None
        self.otp_expiry = None
        self.save(update_fields=['otp', 'otp_expiry'])
        # update_fields=['otp', 'otp_expiry'] → only save THESE two columns
        # This is more efficient than saving the entire user row.
