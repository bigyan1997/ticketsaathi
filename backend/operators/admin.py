from django.contrib import admin
from .models import Operator


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'is_verified', 'created_at')
    list_filter = ('is_verified',)
    search_fields = ('company_name', 'user__email', 'registration_number')
    ordering = ('-created_at',)
