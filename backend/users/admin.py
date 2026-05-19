from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Columns shown in the user list page
    list_display = ('email', 'full_name', 'is_customer', 'is_operator', 'is_staff', 'created_at')
    list_filter = ('is_customer', 'is_operator', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('-created_at',)

    # Fields shown when viewing/editing a user
    fieldsets = (
        ('Login',    {'fields': ('email', 'password')}),
        ('Personal', {'fields': ('full_name', 'phone_number', 'preferred_language')}),
        ('Roles',    {'fields': ('is_customer', 'is_operator')}),
        ('Access',   {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # Fields shown when creating a new user via admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'is_customer', 'is_operator'),
        }),
    )

    # Our login field is email, not username
    USERNAME_FIELD = 'email'
