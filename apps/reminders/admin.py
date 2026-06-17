from django.contrib import admin
from .models import VehicleReminder


@admin.register(VehicleReminder)
class VehicleReminderAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'reminder_type', 'due_date', 'is_completed')
    list_filter = ('reminder_type', 'is_completed')
    search_fields = ('title', 'user__phone_number')
