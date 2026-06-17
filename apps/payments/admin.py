from django.contrib import admin
from .models import Payment, Wallet


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_ref', 'user', 'entity_type', 'amount_egp', 'method', 'status', 'created_at')
    list_filter = ('entity_type', 'method', 'status')
    search_fields = ('transaction_ref', 'user__phone_number')


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'updated_at')
    search_fields = ('user__phone_number',)
