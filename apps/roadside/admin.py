from django.contrib import admin
from .models import RoadsideRequest


@admin.register(RoadsideRequest)
class RoadsideRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_type', 'status', 'created_at', 'estimated_arrival_minutes')
    list_filter = ('service_type', 'status')
    search_fields = ('user__phone_number',)
