from django.contrib import admin
from .models import Station, FuelType, StationSlot, StationReview


class FuelTypeInline(admin.TabularInline):
    model = FuelType
    extra = 1


class StationSlotInline(admin.TabularInline):
    model = StationSlot
    extra = 0


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'address', 'is_active', 'is_24_hours')
    list_filter = ('brand', 'is_active', 'is_24_hours')
    search_fields = ('name', 'brand', 'address')
    inlines = [FuelTypeInline, StationSlotInline]


@admin.register(StationReview)
class StationReviewAdmin(admin.ModelAdmin):
    list_display = ('station', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('station__name', 'user__phone_number')
