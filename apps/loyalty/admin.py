from django.contrib import admin
from .models import LoyaltyAccount, LoyaltyTransaction


@admin.register(LoyaltyAccount)
class LoyaltyAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'tier', 'total_points_earned', 'updated_at')
    list_filter = ('tier',)
    search_fields = ('user__phone_number',)


@admin.register(LoyaltyTransaction)
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'transaction_type', 'description', 'created_at')
    list_filter = ('transaction_type',)
    search_fields = ('user__phone_number',)
