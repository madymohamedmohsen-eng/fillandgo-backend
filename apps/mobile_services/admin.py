from django.contrib import admin
from .models import ServiceProvider, MobileServiceRequest


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'rating', 'is_available')
    search_fields = ('name', 'phone_number')


@admin.register(MobileServiceRequest)
class MobileServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_type', 'status', 'scheduled_time', 'provider')
    list_filter = ('service_type', 'status')
    search_fields = ('user__phone_number',)
