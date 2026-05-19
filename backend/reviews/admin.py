from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'trip', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('user__email', 'trip__route__origin', 'trip__route__destination')
    ordering = ('-created_at',)
