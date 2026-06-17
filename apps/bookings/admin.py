from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_ref', 'user', 'station', 'status', 'scheduled_time', 'amount_egp')
    list_filter = ('status', 'payment_method')
    search_fields = ('booking_ref', 'user__phone_number', 'station__name')
    readonly_fields = ('booking_ref', 'qr_code', 'cars_ahead', 'created_at')
