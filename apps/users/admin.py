from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Vehicle


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('phone_number',)
    list_display = ('phone_number', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('phone_number', 'username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('phone_number', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'username', 'email', 'password1', 'password2'),
        }),
    )


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'user', 'make', 'model', 'year', 'fuel_type', 'is_primary')
    list_filter = ('fuel_type', 'is_primary')
    search_fields = ('license_plate', 'user__phone_number', 'make', 'model')
